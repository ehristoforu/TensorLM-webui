import os
import random
import sys

from modules.inference import load_model, generate_text
from modules.openai_api import chat_openai

def process_to_run(message, history, mode, system_prompt, preset, temperature, max_tokens, top_p, top_k, repeat_penalty, model, n_ctx, n_gpu_layers, n_threads, verbose, f16_kv, logits_all, vocab_only, use_mmap, use_mlock, n_batch, last_n_tokens_size, low_vram, rope_freq_base, rope_freq_scale):
    if mode == "Local":
        generate_text(message, history, system_prompt, preset, temperature, max_tokens, top_p, top_k, repeat_penalty, model, n_ctx, n_gpu_layers, n_threads, verbose, f16_kv, logits_all, vocab_only, use_mmap, use_mlock, n_batch, last_n_tokens_size, low_vram, rope_freq_base, rope_freq_scale)
    elif mode == "OpenAI":
        chat_openai(message, history, system_prompt, preset, temperature, max_tokens, top_p)