from utils import batch_generate, parse_csv
import argparse
import json
import os

def main():
    parser = argparse.ArgumentParser(description="Init words")
    parser.add_argument("--target_language", type=str, required=True)
    parser.add_argument("--native_language", type=str, required=True)
    parser.add_argument("--chunk_size", type=int, required=True)
    parser.add_argument("--word_bank_path", type=str, required=True)
    parser.add_argument("--api_url", type=str, default="")
    parser.add_argument("--api_key_env", type=str, default="")
    parser.add_argument("--model", type=str, default="")
    parser.add_argument("--output_file", type=str, default="sets/words.json")

    args = parser.parse_args()

    with open(args.word_bank_path, "r", encoding="utf-8") as f:
        words = [line.strip() for line in f if line.strip()]

    script_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(script_dir, "prompts", "init.md"), "r", encoding="utf-8") as f:
        prompt_template = f.read()

    chunks = [words[i:i + args.chunk_size] for i in range(0, len(words), args.chunk_size)]
    
    inputs = []
    for chunk in chunks:
        word_bank_str = "\n".join(chunk)
        prompt = prompt_template.replace("{{target_language}}", args.target_language) \
                                .replace("{{native_language}}", args.native_language) \
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

    chunk_dicts = []
    seen_words = set()

    for chunk, text in zip(chunks, texts):
        rows = parse_csv(text)
        if len(rows) != len(chunk) + 1:
            print(f"Error: Expected {len(chunk) + 1} rows, got {len(rows)}")
            print(f"Text: {text}")
            continue
            
        header = rows[0]
        data_rows = rows[1:]
        
        current_chunk_dicts = []
        for row in data_rows:
            d = {}
            for i, val in enumerate(row):
                if i >= len(header):
                    print(f"Error: Row {row} has more columns than header")
                    print(f"Header: {header}")
                    break
                key = header[i]
                d[key] = val
            
            word = d.get("word", "").strip()
            if not word:
                print(f"Error: Row {row} has no word")
                continue
            if word not in seen_words:
                seen_words.add(word)
                d["sentences"] = []
                current_chunk_dicts.append(d)
            else:
                print(f"Error: Word {word} is already in the list")
        
        chunk_dicts.append(current_chunk_dicts)

    all_dicts = []
    max_len = max((len(c) for c in chunk_dicts), default=0)
    for i in range(max_len):
        for c_dicts in chunk_dicts:
            if i < len(c_dicts):
                all_dicts.append(c_dicts[i])

    os.makedirs(os.path.dirname(args.output_file), exist_ok=True)
    with open(args.output_file, "w", encoding="utf-8") as f:
        json.dump(all_dicts, f, indent=4, ensure_ascii=False)

    print(f"\n--- Summary Stats ---")
    print(f"Input words: {len(words)}")
    print(f"Chunks processed: {len(inputs)}")
    print(f"Words extracted: {len(all_dicts)}")
    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Completion tokens: {completion_tokens}")
    print(f"Total tokens: {prompt_tokens + completion_tokens}")
    print(f"Saved to: {args.output_file}")

if __name__ == "__main__":
    main()
