import os
import random
import time
import gradio as gr

def mode_change(mode):
    if mode == "Local":
        return gr.update(interactive=True), gr.update(interactive=True), gr.update(interactive=True), gr.update(interactive=True)
    elif mode == "OpenAI":
        return gr.update(interactive=False), gr.update(interactive=False), gr.update(interactive=False), gr.update(interactive=False)