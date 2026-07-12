import asyncio
import csv
import io
import re
from openai import AsyncOpenAI

MAX_RETRIES = 5

MAX_CONCURRENT = 256

async def _send_request(
    client: AsyncOpenAI,
    semaphore: asyncio.Semaphore,
    messages: list[dict],
    model_name: str = "",
) -> tuple[str, int, int]:
    """Send a single chat completion request. Retries are handled by the OpenAI client."""
    async with semaphore:
        try:
            response = await client.chat.completions.create(model=model_name, messages=messages)
            usage = getattr(response, "usage", None)
            prompt_tokens = usage.prompt_tokens if usage else 0
            completion_tokens = usage.completion_tokens if usage else 0
            return response.choices[0].message.content or "", prompt_tokens, completion_tokens
        except Exception as e:
            print(f"Request failed: {e}")
            return "", 0, 0

async def _batch_generate_async(
    api_url: str,
    inputs: list[list[dict]],
    api_key: str = "EMPTY",
    model_name: str = "",
) -> tuple[list[str], int, int]:
    """Fires requests concurrently with a bounded semaphore."""
    client = AsyncOpenAI(
        base_url=api_url,
        api_key=api_key,
        max_retries=MAX_RETRIES,
        timeout=360.0,
    )
    semaphore = asyncio.Semaphore(MAX_CONCURRENT)
    total = len(inputs)
    completed = 0

    async def _tracked_request(messages: list[dict]) -> tuple[str, int, int]:
        nonlocal completed
        result = await _send_request(client, semaphore, messages, model_name=model_name)
        completed += 1
        if completed % 100 == 0 or completed == total:
            print(f"  Progress: {completed}/{total} requests complete", flush=True)
        return result

    tasks = [_tracked_request(messages) for messages in inputs]
    results = await asyncio.gather(*tasks)
    await client.close()
    texts = [r[0] for r in results]
    prompt_tokens = sum(r[1] for r in results)
    completion_tokens = sum(r[2] for r in results)
    return texts, prompt_tokens, completion_tokens

def batch_generate(
    api_url: str,
    inputs: list[list[dict]],
    api_key: str = "EMPTY",
    model_name: str = "",
) -> tuple[list[str], int, int]:
    """
    Takes in a list of OpenAI compatible chat conversations, and returns a list of responses.
    Uses the async OpenAI client to fire all requests concurrently via asyncio.gather.

    Args:
        api_url: The URL of the OpenAI-compatible chat completions endpoint
                 (e.g. "http://localhost:8000/v1").
        inputs: A list of conversations, where each conversation is a list of
            {"role": ..., "content": ...} message dicts.

    Returns:
        A tuple of (list of assistant response strings, total prompt tokens, total completion tokens).
    """
    return asyncio.run(_batch_generate_async(api_url, inputs, api_key, model_name))

def parse_csv(text):
    match = re.search(r'```(?:csv)?\n(.*?)\n```', text, re.DOTALL)
    csv_string = match.group(1).strip() if match else ""
    
    if not csv_string:
        return []
    
    delimiter = '|' if '|' in csv_string.split('\n')[0] else ','
    reader = csv.reader(io.StringIO(csv_string), delimiter=delimiter)
    
    return [[col.strip() for col in row] for row in reader if row]