# Yet Another Language Learning App

Powered by human stupidity!

*Artificial Intelligence not included™*

**Instructions:**

1. ``uv venv --python 3.12``
2. ``uv sync``
3. ``uv pip install vllm --torch-backend cu130`` (or whatever engine you want to use, or you can use an api)
4. 
```
vllm serve google/gemma-4-31B-it-qat-w4a16-ct \
   --pipeline-parallel-size 4 \
   --trust-remote-code \
   --max-model-len 64000 \
   --max-num-seqs 32 \
   --default-chat-template-kwargs '{"enable_thinking": false}'
```
Or whatever model you prefer.
5.
``python set_maker/init.py --target_language japanese --native_language english --chunk_size 100 --word_bank_path word_banks/japanese.csv --api_url http://localhost:8000/v1``, replacing api url with your url and the language/word bank with the appropriate values.
6. 