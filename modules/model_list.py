import os
import gradio as gr
import copy
import llama_cpp
from llama_cpp import Llama
import random
from huggingface_hub import hf_hub_download  
import time

def list_models(name):
    dir = os.getcwd()
    return os.listdir(f"{dir}\models")