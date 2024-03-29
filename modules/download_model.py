import os
import gradio as gr
import copy
import llama_cpp
from llama_cpp import Llama
import random
from huggingface_hub import hf_hub_download  
import time

def download_model(repo_id, filename):
    hf_hub_download(
        repo_id=repo_id,
        filename=filename,
        local_dir="models",
        force_download=True, resume_download=False,
        cache_dir=".cache",
    )
    return f"Downloaded!"