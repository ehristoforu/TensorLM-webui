
from modules.load_configure import *
import time

if echo == "True":
    from modules.echo import *


import os
import gradio as gr
import copy
import llama_cpp
from llama_cpp import Llama
import random
from huggingface_hub import hf_hub_download  

from modules.download_model import download_model
from modules.inference import generate_text
from modules.load_model import load_model
from modules.openai_api import chat_openai
from modules.change import mode_change
from modules.model_list import list_models
from modules.render_markdown import render_md
from modules.load_presets import load_presets_names, load_presets_value
from modules.arg_parser import *

#from blip.blip_engine import blip_run

dir = os.getcwd()

if footer == "True":
    footer_vis = True
else:
    footer_vis = False

history = []

    
chatbot = gr.Chatbot(show_label=False, layout=chat_style, show_copy_button=True, height=500, min_width=180, bubble_full_width=False)

with gr.Blocks(theme=theme, title=f"TensorLM v{tlm_version}", css="style.css") as webui:
    #refresh_model = gr.Button(value="Load model", interactive=True, scale=1)
    with gr.Row():
        with gr.Row(render=False, variant="panel") as sliders:       
            with gr.Tab("Parameters"):
                mode = gr.Radio(label="Mode", choices=["Local", "OpenAI", "MistralAI"], value="Local", interactive=True)
                openai_endpoint = gr.Dropdown(label="OpenAI Endpoint", choices=["api.chatanywhere.tech/v1", "api.openai.com/v1", "api.naga.ac/v1", "chatgpt-api.shn.hk/v1"], value="api.chatanywhere.tech/v1", allow_custom_value=True, interactive=True, visible=False)
                openai_model = gr.Dropdown(label="OpenAI Model", choices=["gpt-3.5-turbo", "gpt-3.5-turbo-16k", "gpt-3.5-turbo-0301", "gpt-4", "gpt-4-0314", "gpt-4-0613"], value="gpt-3.5-turbo", allow_custom_value=True, interactive=True, visible=False)
                mistralai_model = gr.Dropdown(label="MistralAI Model", choices=["mixtral-8x7b", "mistral-7b"], value="mixtral-8x7b", allow_custom_value=False, interactive=True, visible=False)
                max_tokens = gr.Slider(label="Max new tokens", minimum=256, maximum=4056, value=512, step=8, interactive=True)
                temperature = gr.Slider(label="Temperature", minimum=0.01, maximum=2.00, value=0.15, step=0.01, interactive=True)
                top_p = gr.Slider(label="Top P", minimum=0.01, maximum=2.00, value=0.10, step=0.01, interactive=True)
                top_k = gr.Slider(label="Top K", minimum=10.00, maximum=100.00, value=40.00, step=0.01, interactive=True)
                repeat_penalty = gr.Slider(label="Repeat penalty", minimum=0.01, maximum=2.00, value=1.10, step=0.01, interactive=True)
            with gr.Tab("Instructions"):
                preset = gr.Radio(label="Prompt preset", choices=load_presets_names(), value=load_presets_names()[1], interactive=True)
                system_prompt = gr.Textbox(label="Custom system prompt", max_lines=4, lines=3, interactive=True)
            with gr.Tab("Model"):
                model = gr.Dropdown(label="Model (only based on Llama in GGML/GGUF format (.bin/.gguf))", choices=os.listdir(f"{dir}/models"), value="None", interactive=True, allow_custom_value=False, scale=50)

        
        with gr.Row(render=False) as settings:
            reload_model = gr.Button("Apply settings to model", interactive=True)
            n_ctx = gr.Slider(label="Number of CTX", minimum=1024, maximum=4056, value=2048, step=8, interactive=True)
            n_gpu_layers = gr.Slider(label="Number of GPU layers", minimum=0, maximum=36, value=0, step=1, interactive=True)
            n_threads = gr.Slider(label="Number of Threads", minimum=2, maximum=36, value=4, step=1, interactive=True)
            verbose = gr.Checkbox(label="Verbose", value=True, interactive=True)
            f16_kv = gr.Checkbox(label="F16 KV", value=True, interactive=True)
            logits_all = gr.Checkbox(label="Logits all", value=False, interactive=True)
            vocab_only = gr.Checkbox(label="Vocab only", value=False, interactive=True)
            use_mmap = gr.Checkbox(label="Use mmap", value=True, interactive=True)
            use_mlock = gr.Checkbox(label="Use mlock", value=False, interactive=True)
            n_batch = gr.Slider(label="Number of batch", minimum=128, maximum=2048, value=512, step=8, interactive=True)
            last_n_tokens_size = gr.Slider(label="Last number of tokens size", minimum=8, maximum=512, value=64, step=8, interactive=True)
            low_vram = gr.Checkbox(label="Low VRAM", value=lowvram_arg, interactive=True)
            rope_freq_base = gr.Slider(label="Rope freq base", minimum=1000.0, maximum=30000.0, value=10000.0, step=0.1, interactive=True)
            rope_freq_scale = gr.Slider(label="Rope freq scale", minimum=0.1, maximum=3.0, value=1.0, step=0.1)

        with gr.Column(scale=2):
            with gr.Row():
                gr.ChatInterface(
                    generate_text,
                    chatbot=chatbot,
                    retry_btn="🔄️",
                    submit_btn="📨",
                    undo_btn="↩️",
                    clear_btn="🗑️",
                    additional_inputs=[mode, openai_endpoint, openai_model, mistralai_model, system_prompt, preset, temperature, max_tokens, top_p, top_k, repeat_penalty, model, n_ctx, n_gpu_layers, n_threads, verbose, f16_kv, logits_all, vocab_only, use_mmap, use_mlock, n_batch, last_n_tokens_size, low_vram, rope_freq_base, rope_freq_scale]
                )
            with gr.Row():
                options_change = gr.Checkbox(label="Options", value=False, interactive=True)
                tabs_change = gr.Checkbox(label="Tabs", value=False, interactive=True)
            with gr.Row():
                with gr.Row(visible=False) as tabs:
                    with gr.Tab("ModelGet"):
                        gr.Markdown("## Download model from 🤗 HuggingFace.co")
                        with gr.Row():
                            repo_id = gr.Textbox(label="REPO_ID",  value="ehristoforu/LLMs", lines=1, max_lines=1, interactive=False)
                            filename = gr.Dropdown(label="FILENAME", interactive=True, choices=["llama-2-7b-chat.ggmlv3.q2_K.bin", "llama-2-13b-chat.ggmlv3.q2_K.bin", "codellama-7b-instruct.ggmlv3.Q2_K.bin", "codellama-13b-instruct.ggmlv3.Q2_K.bin", "saiga-13b.ggmlv3.Q4_1.bin", "saiga-30b.ggmlv3.Q3_K.bin"], value="", allow_custom_value=False)
                            download_btn = gr.Button(value="Download")
                            logs=gr.Markdown()
                    with gr.Tab("Notebook"):
                        with gr.Row():
                            with gr.Column(scale=1):
                                render_markdown = gr.Button(value="Render markdown", interactive=True)
                                notebook = gr.Textbox(show_label=False, value="This is a great day...", placeholder="Your notebook", max_lines=40, lines=35, interactive=True, show_copy_button=True)
                            with gr.Row():
                                with gr.Column(scale=1):
                                    markdown = gr.Markdown()
                

                    with gr.Tab("Settings"):
                        with gr.Row():
                            with gr.Column():
                                #with gr.Row():
                                #    gr.Markdown("### Style")
                                #    chat_style = gr.Dropdown(label="Style of chat", choices=["bubble", "panel"], value="bubble", interactive=True, allow_custom_value=False)
                                settings.render()
            with gr.Row():
                gr.Markdown(f"""
                <center><a href="https://github.com/ehristoforu/TensorLM-webui">v{tlm_version}</a> | <a href="/?view=api">API</a> | <a href="https://gradio.app">gradio 4.1.2</a> | <a href="https://github.com/ggerganov/llama.cpp">llama.cpp</a> | <a href="https://python.org">python</a> | <a href="https://huggingface.co/TheBloke?search_models=GGML">Suggested models</a></center>
                """, visible=footer_vis)      

    
        with gr.Row(visible=False) as options:
            with gr.Column(scale=1):
                sliders.render()
     
    mode.change(
        fn=mode_change,
        inputs=mode,
        outputs=[top_k, repeat_penalty, model, reload_model, openai_endpoint, openai_model, mistralai_model],
        queue=False,
        api_name=False,
    )
    render_markdown.click(
        fn=render_md,
        inputs=notebook,
        outputs=markdown,
        queue=False,
        api_name=False,
    )
    notebook.change(
        fn=render_md,
        inputs=notebook,
        outputs=markdown,
        queue=False,
        api_name=False,
    )

    options_change.change(
        fn=lambda x: gr.update(visible=x),
        inputs=options_change,
        outputs=options,
        queue=False,
        api_name=False,
    )
    tabs_change.change(
        fn=lambda x: gr.update(visible=x),
        inputs=tabs_change,
        outputs=tabs,
        queue=False,
        api_name=False,
    )

    


    download_btn.click(download_model, inputs=[repo_id, filename], outputs=logs, api_name=False, queue=False)
                
    model.change(load_model, inputs=[model, n_ctx, n_gpu_layers, n_threads, verbose, f16_kv, logits_all, vocab_only, use_mmap, use_mlock, n_batch, last_n_tokens_size, low_vram, rope_freq_base, rope_freq_scale], outputs=model, api_name=False, queue=False)
    reload_model.click(load_model, inputs=[model, n_ctx, n_gpu_layers, n_threads, verbose, f16_kv, logits_all, vocab_only, use_mmap, use_mlock, n_batch, last_n_tokens_size, low_vram, rope_freq_base, rope_freq_scale], outputs=model, api_name=False, queue=False)



webui.launch(
    inbrowser=inbrowser_arg,
    debug=debug_arg,
    quiet=quiet_arg,
    favicon_path="assets/favicon.png",
    show_api=show_api,
    share_server_protocol=share_server_protocol,
)
