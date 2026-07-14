from utils import batch_generate, parse_csv
import argparse
import json
import os
import random

def main():
    parser = argparse.ArgumentParser(description="Generate sentences for words")
    parser.add_argument("--target_language", type=str, required=True)
    parser.add_argument("--native_language", type=str, required=True)
    parser.add_argument("--chunk_size", type=int, required=True)
    parser.add_argument("--input_file", type=str, default="sets/words.json")
    parser.add_argument("--output_file", type=str, default="sets/final.json")
    parser.add_argument("--api_url", type=str, default="")
    parser.add_argument("--api_key_env", type=str, default="")
    parser.add_argument("--model", type=str, default="")
    parser.add_argument("--shuffle", action="store_true", help="Shuffle word bank before chunking, without seeding.")

    args = parser.parse_args()

    with open(args.input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    all_words = [d["word"] for d in data]
    all_words_str = ", ".join(all_words)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "prompts", "sentences.md"), "r", encoding="utf-8") as f:
        prompt_template = f.read()

    indices = list(range(len(data)))
    if args.shuffle:
        random.shuffle(indices)

    chunks_indices = [indices[i:i + args.chunk_size] for i in range(0, len(indices), args.chunk_size)]
    
    inputs = []
    for chunk in chunks_indices:
        word_bank = [data[i]["word"] for i in chunk]
        word_bank_str = "\n".join(word_bank)
        
        prompt = prompt_template.replace("{{target_language}}", args.target_language) \
                                .replace("{{native_language}}", args.native_language) \
                                .replace("{{words}}", all_words_str) \
                                .replace("{{word_bank}}", word_bank_str)
        inputs.append([{"role": "user", "content": prompt}])

    print(f"Sending {len(inputs)} chunks to LLM...")
    api_key = os.environ.get(args.api_key_env, "EMPTY") if args.api_key_env else "EMPTY"
    texts, prompt_tokens, completion_tokens = batch_generate(
        args.api_url, 
        inputs, 
        api_key, 
        args.model
    )

    for chunk_indices, text in zip(chunks_indices, texts):
        rows = parse_csv(text)
        if len(rows) != len(chunk_indices) + 1:
            print(f"Error: Expected {len(chunk_indices) + 1} rows, got {len(rows)}")
            print(f"Text: {text}")
            continue
            
        data_rows = rows[1:]
        
        for i, idx in enumerate(chunk_indices):
            row = data_rows[i]
            if len(row) != 2:
                print(f"Error: Row {row} has {len(row)} columns, expected 2")
                continue

            exert = row[0].strip()
            translation = row[1].strip()

            if "[" not in exert or "]" not in exert:
                print(f"Error: Row {row} has no \"[]\"")
                continue

            is_duplicate = False
            for existing_sentence in data[idx].get("sentences", []):
                if existing_sentence.get("exert", "").strip() == exert or existing_sentence.get("translation", "").strip() == translation:
                    is_duplicate = True
                    break
            
            if is_duplicate:
                print(f"Skipping duplicate sentence for word {data[idx]['word']}")
                continue

            data[idx]["sentences"].append({
                    "exert": exert,
                    "translation": translation
                })

    os.makedirs(os.path.dirname(args.output_file), exist_ok=True)
    with open(args.output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"\n--- Summary Stats ---")
    print(f"Words processed: {len(data)}")
    print(f"Chunks processed: {len(inputs)}")
    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Completion tokens: {completion_tokens}")
    print(f"Total tokens: {prompt_tokens + completion_tokens}")
    print(f"Saved to: {args.output_file}")

if __name__ == "__main__":
    main()
