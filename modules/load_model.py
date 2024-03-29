import os
import gradio as gr
import copy
import llama_cpp
from llama_cpp import Llama
import random
from huggingface_hub import hf_hub_download  
import time

def load_model(path, n_ctx, n_gpu_layers, n_threads, verbose, f16_kv, logits_all, vocab_only, use_mmap, use_mlock, n_batch, last_n_tokens_size, low_vram, rope_freq_base, rope_freq_scale):
    try:
        dir = os.getcwd()
        global llm
        llm = Llama(
            model_path=f"{dir}\models\{path}",
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
        return path 
    except:
        return ""