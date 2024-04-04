import os
import gradio as gr
import copy
import llama_cpp
from llama_cpp import Llama
import random
from huggingface_hub import hf_hub_download  
import time

from modules.load_presets import load_presets_value
from modules.load_model import *

def generate_text(message, history, system_prompt, preset, temperature, max_tokens, top_p, top_k, repeat_penalty, model, n_ctx, n_gpu_layers, n_threads, verbose, f16_kv, logits_all, vocab_only, use_mmap, use_mlock, n_batch, last_n_tokens_size, low_vram, rope_freq_base, rope_freq_scale):
    dir = os.getcwd()
    global llm
    llm = Llama(
        model_path=f"{dir}\models\{model}",
        n_ctx=n_ctx,
        n_gpu_layers=n_gpu_layers,
        n_threads=n_threads,
        verbose=verbose,
        f16_kv=f16_kv,
        logits_all=logits_all,
        vocab_only=vocab_only,
        use_mmap=use_mmap,
        use_mlock=use_mlock,
        n_batch=n_batch,
        last_n_tokens_size=last_n_tokens_size,
        low_vram=low_vram,
        rope_freq_base=rope_freq_base,
        rope_freq_scale=rope_freq_scale,



    )
    global_sys_prompt = load_presets_value(preset) + " " + system_prompt
    temp = ""
    input_prompt = f"[INST] <<SYS>>\n{global_sys_prompt}.\n<</SYS>>\n\n "
    for interaction in history:
        input_prompt = input_prompt + str(interaction[0]) + " [/INST] " + str(interaction[1]) + " </s><s> [INST] "

    input_prompt = input_prompt + str(message) + " [/INST] "

    output = llm(
        input_prompt,
        temperature=temperature,
        top_p=top_p,
        top_k=top_k, 
        repeat_penalty=repeat_penalty,
        max_tokens=max_tokens,
        stop=[
            "<|prompter|>",
            "<|endoftext|>",
            "<|endoftext|> \n",
            "ASSISTANT:",
            "USER:",
            "SYSTEM:",
        ],
        stream=True,
    )
    for out in output:
        stream = copy.deepcopy(out)
        temp += stream["choices"][0]["text"]
        yield temp

    history = ["init", input_prompt]
