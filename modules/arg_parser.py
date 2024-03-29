import os
import gradio as gr
import copy
import llama_cpp
from llama_cpp import Llama
import random
from huggingface_hub import hf_hub_download  
import time
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--inbrowser", action="store_true", help="Run in browser")
parser.add_argument("--share", action="store_true", help="Run in share mode with public url")
parser.add_argument("--debug", action="store_true", help="Run in debug mode for dev")
parser.add_argument("--quiet", action="store_true", help="Run in quiet mode without many console trash logs")
parser.add_argument("--lowvram", action="store_true", help="Run in low vram mode")


args = parser.parse_args()


global inbrowser_arg
inbrowser_arg = args.inbrowser

global share_arg
share_arg = args.share

global debug_arg
debug_arg = args.debug

global quiet_arg
quiet_arg = args.quiet

global lowvram_arg
lowvram_arg = args.lowvram