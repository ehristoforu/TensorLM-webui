from openai import OpenAI
import gradio as gr
import os
import time
import random

from modules.load_configure import *
from modules.load_presets import load_presets_value

client = OpenAI(api_key=openai_key, base_url="https://api.chatanywhere.tech/v1")

def chat_openai(message, history, system_prompt, preset, temperature, max_tokens, top_p):
    global_sys_prompt = load_presets_value(preset) + " " + system_prompt
    
    history_openai_format = []
    history_openai_format.append({"role": "user", "content":  global_sys_prompt})
    for human, assistant in history:
        history_openai_format.append({"role": "user", "content": human })
        history_openai_format.append({"role": "assistant", "content":assistant})
    history_openai_format.append({"role": "user", "content": message})
  
    response = client.chat.completions.create(model='gpt-3.5-turbo',
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