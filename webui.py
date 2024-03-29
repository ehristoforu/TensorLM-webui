
from art import *
import time

print(text2art('''TensorLM''', font="small"))
print("Our license: https://www.apache.org/licenses/LICENSE-2.0.txt")


time.sleep(5)

print(" ")

import os
import gradio as gr
import copy
import llama_cpp
from llama_cpp import Llama
import random
from huggingface_hub import hf_hub_download  

#from blip.blip_engine import blip_run



dir = os.getcwd()

def load_model(path, n_ctx, n_gpu_layers, n_threads, verbose, f16_kv, logits_all, vocab_only, use_mmap, use_mlock, n_batch, last_n_tokens_size, low_vram, rope_freq_base, rope_freq_scale):
    try:
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

def list_models(name):
    return os.listdir(f"{dir}\models")

def render_md(text):
    return f"{text}"

def download_model(repo_id, filename):
    hf_hub_download(
        repo_id=repo_id,
        filename=filename,
        local_dir="models",
        force_download=True, resume_download=False,
        cache_dir=".cache",
    )
    return f"Downloaded!"

history = []

'''
system_message = """
You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe.  Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.
If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.
"""
'''


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


    
chatbot = gr.Chatbot(show_label=False, layout="panel", show_copy_button=True, height=500, min_width=180)

with gr.Blocks(theme="theme-repo/STONE_Theme", title="TensorLM", css="style.css") as demo:
    with gr.Row():
        model = gr.Dropdown(label="Model (only based on Llama in GGML format (.bin))", choices=os.listdir(f"{dir}\models"), value="None", interactive=True, allow_custom_value=False, scale=50)
        #refresh_model = gr.Button(value="Load model", interactive=True, scale=1)
    with gr.Row():
        with gr.Tab("💬"):
            with gr.Row(visible=False, render=False) as sliders:
        
                with gr.Tab("Parameters"):
                    max_tokens = gr.Slider(label="Max new tokens", minimum=256, maximum=4056, value=512, step=8, interactive=True)
                    temperature = gr.Slider(label="Temperature", minimum=0.01, maximum=2.00, value=0.15, step=0.01, interactive=True)
                    top_p = gr.Slider(label="Top P", minimum=0.01, maximum=2.00, value=0.10, step=0.01, interactive=True)
                    top_k = gr.Slider(label="Top K", minimum=10.00, maximum=100.00, value=40.00, step=0.01, interactive=True)
                    repeat_penalty = gr.Slider(label="Repeat penalty", minimum=0.01, maximum=2.00, value=1.10, step=0.01, interactive=True)
                with gr.Tab("Instructions"):
                    preset = gr.Dropdown(label="Prompt preset", choices=["AI-assistant", "Historical Expert", "Math Tutor", "Python Tutor", "Language Learning Coach", "Philosopher", "Poet"], value="AI-assistant", interactive=True, allow_custom_value=False)
                    system_prompt = gr.Textbox(label="Custom system prompt", max_lines=4, lines=3, interactive=True)

            with gr.Row():
                gr.ChatInterface(
                    generate_text,
                    chatbot=chatbot,
                    retry_btn="🔄️",
                    submit_btn="📨",
                    undo_btn="↩️",
                    clear_btn="🗑️",
                    additional_inputs=[system_prompt, preset, temperature, max_tokens, top_k, top_k, repeat_penalty]
                )
                

            sliders_change = gr.Checkbox(label="Options", value=False, interactive=True)
            with gr.Row():
                sliders.render()
            

        with gr.Tab("💽"):
            gr.Markdown("## Download model from 🤗 HuggingFace.co")
            with gr.Row():
                repo_id = gr.Textbox(label="REPO_ID",  value="ehristoforu/LLMs", lines=1, max_lines=1, interactive=False)
                filename = gr.Dropdown(label="FILENAME", interactive=True, choices=["llama-2-7b-chat.ggmlv3.q2_K.bin", "llama-2-13b-chat.ggmlv3.q2_K.bin", "codellama-7b-instruct.ggmlv3.Q2_K.bin", "codellama-13b-instruct.ggmlv3.Q2_K.bin", "saiga-13b.ggmlv3.Q4_1.bin", "saiga-30b.ggmlv3.Q3_K.bin"], value="", allow_custom_value=False)
                download_btn = gr.Button(value="Download")
                logs=gr.Markdown()
        with gr.Tab("📒"):
            with gr.Tab("Notebook"):
                with gr.Row():
                    notebook = gr.Textbox(show_label=False, value="This is a great day...", placeholder="Your notebook", max_lines=40, lines=35, interactive=True)
            with gr.Tab("Markdown"):
                render_markdown = gr.Button(value="Render markdown from Notebook", interactive=True)
                with gr.Row():
                    markdown = gr.Markdown()

        with gr.Tab("⚙️"):
            with gr.Row():
                with gr.Column():
                    #with gr.Row():
                    #    gr.Markdown("### Style")
                    #    chat_style = gr.Dropdown(label="Style of chat", choices=["bubble", "panel"], value="bubble", interactive=True, allow_custom_value=False)
                    with gr.Row():
                        gr.Markdown("### Engine")
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
                        low_vram = gr.Checkbox(label="Low VRAM", value=False, interactive=True)
                        rope_freq_base = gr.Slider(label="Rope freq base", minimum=1000.0, maximum=30000.0, value=10000.0, step=0.1, interactive=True)
                        rope_freq_scale = gr.Slider(label="Rope freq scale", minimum=0.1, maximum=3.0, value=1.0, step=0.1)

    with gr.Row():
        gr.Markdown("""
        <center><a href="https://gradio.app">gradio 4.1.0</a> | <a href="https://github.com/ggerganov/llama.cpp">llama.cpp</a> | <a href="https://python.org">python</a> | <a href="https://huggingface.co/TheBloke?search_models=GGML">Suggested models</a></center>
        """)    
    
    render_markdown.click(
        fn=render_md,
        inputs=notebook,
        outputs=markdown,
        queue=False,
        api_name=False,
    )

    sliders_change.change(
        fn=lambda x: gr.update(visible=x),
        inputs=sliders_change,
        outputs=sliders,
        queue=False,
        api_name=False,
    )

    


    download_btn.click(download_model, inputs=[repo_id, filename], outputs=logs, api_name=False, queue=False)
                
    model.change(load_model, inputs=[model, n_ctx, n_gpu_layers, n_threads, verbose, f16_kv, logits_all, vocab_only, use_mmap, use_mlock, n_batch, last_n_tokens_size, low_vram, rope_freq_base, rope_freq_scale], outputs=model, api_name=False, queue=False)
    reload_model.click(load_model, inputs=[model, n_ctx, n_gpu_layers, n_threads, verbose, f16_kv, logits_all, vocab_only, use_mmap, use_mlock, n_batch, last_n_tokens_size, low_vram, rope_freq_base, rope_freq_scale], outputs=model, api_name=False, queue=False)



demo.launch(
    inbrowser=True,
    server_port=5555,
    debug=False,
    quiet=True,
    favicon_path="assets/favicon.png",
)