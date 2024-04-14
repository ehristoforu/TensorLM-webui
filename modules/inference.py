import os
import gradio as gr
import copy
import llama_cpp
from llama_cpp import Llama
import random
from huggingface_hub import hf_hub_download, InferenceClient 
import time

from modules.load_presets import load_presets_value
from modules.load_configure import *
from modules.load_model import *

def generate_text(message, history, mode, openai_endpoint, openai_model, mistralai_model, system_prompt, preset, temperature, max_tokens, top_p, top_k, repeat_penalty, model, n_ctx, n_gpu_layers, n_threads, verbose, f16_kv, logits_all, vocab_only, use_mmap, use_mlock, n_batch, last_n_tokens_size, low_vram, rope_freq_base, rope_freq_scale):
    global_sys_prompt = load_presets_value(preset) + " " + system_prompt
    
    if mode == "Local":
        dir = os.getcwd()
        global llm
        llm = Llama(
            model_path=f"{dir}/models/{model}",
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
    elif mode == "OpenAI":
        from openai import OpenAI
        
        client = OpenAI(api_key=openai_key, base_url=f"https://{openai_endpoint}")
    
        history_openai_format = []
        history_openai_format.append({"role": "user", "content":  global_sys_prompt})
        for human, assistant in history:
            history_openai_format.append({"role": "user", "content": human })
            history_openai_format.append({"role": "assistant", "content":assistant})
        history_openai_format.append({"role": "user", "content": message})
    
        response = client.chat.completions.create(model=openai_model,
        messages= history_openai_format,
        max_tokens=max_tokens,
        top_p=top_p,
        temperature=temperature,
        stream=True)

        partial_message = ""
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                partial_message = partial_message + chunk.choices[0].delta.content
                yield partial_message
    elif mode == "MistralAI":
        if mistralai_model == "mixtral-8x7b":
            client = InferenceClient(
                "mistralai/Mixtral-8x7B-Instruct-v0.1"
            )
        elif mistralai_model == "mistral-7b":
            client = InferenceClient(
                "mistralai/Mistral-7B-Instruct-v0.2"
            )


        def format_prompt(message, history):
            prompt = "<s>"
            for user_prompt, bot_response in history:
                prompt += f"[INST] {user_prompt} [/INST]"
                prompt += f" {bot_response}</s> "
            prompt += f"[INST] {message} [/INST]"
            return prompt

        temperature = float(temperature)
        if temperature < 1e-2:
            temperature = 1e-2
        top_p = float(top_p)

        generate_kwargs = dict(
            temperature=temperature,
            max_new_tokens=max_tokens,
            top_p=top_p,
            repetition_penalty=repeat_penalty,
            do_sample=True,
            seed=42,
        )

        formatted_prompt = format_prompt(f"{global_sys_prompt}, {message}", history)
        stream = client.text_generation(formatted_prompt, **generate_kwargs, stream=True, details=True, return_full_text=False)
        output = ""

        for response in stream:
            output += response.token.text
            yield output
        return output