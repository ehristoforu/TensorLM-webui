import os
import gradio as gr
import copy
import llama_cpp
from llama_cpp import Llama
import random
from huggingface_hub import hf_hub_download  
import time

def generate_text(message, history, system_prompt, preset, temperature, max_tokens, top_p, top_k, repeat_penalty):
    temp = ""
    input_prompt = f"[INST] <<SYS>>\nYou are {preset}. {system_prompt}.\n<</SYS>>\n\n "
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
