import gradio as gr
import os

# Retrieve the token from environment variables
hf_token = os.getenv("HF_TOKEN")

# Load the interface from the private Space
chat = gr.load("soma-hf/soma-conversation", hf_token=hf_token, src="spaces")

chat.launch()