import os
import random
import time
import gradio as gr

def mode_change(mode):
    if mode == "Local":
        return gr.update(interactive=True), gr.update(interactive=True), gr.update(interactive=True), gr.update(interactive=True), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False)
    elif mode == "OpenAI":
        return gr.update(interactive=False), gr.update(interactive=False), gr.update(interactive=False), gr.update(interactive=False), gr.update(visible=True), gr.update(visible=True), gr.update(visible=False)
    elif mode == "MistralAI":
        return gr.update(interactive=False), gr.update(interactive=True), gr.update(interactive=False), gr.update(interactive=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=True)