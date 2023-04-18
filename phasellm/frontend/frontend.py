"""
Package for interfacing with PhaseLLM via a web browser. We recommend using this code only for local testing and exploration.
"""

from flask import Flask, request, render_template

"""
# Code for testing this...
import phasellm.frontend.frontend as fe
from phasellm.llms import GPT2Wrapper
m1 = GPT2Wrapper()
fe.MODELS = [m1]
fe.run()
"""

MODELS = [] # Add models you wantto test to this variable.

APP = Flask(__name__)

@APP.route("/text_completion", methods = ['POST'])
def text_completion():
    """
    POST-only URL that returns text completion for all models.
    """

    text_to_complete = request.json["input"]

    outputs = []
    for m in MODELS:
        output = m.text_completion(text_to_complete)
        outputs.append({"model":str(m), "content":output})

    return {"status":"ok", "outputs":outputs}

@APP.route("/chat_completion", methods = ['POST'])
def complete_chat():
    """
    POST-only URL that returns chat responses for all models.
    """

    chat_content = request.json["input"]

    messages = [{"role":"system", "content":"You are a friendly chatbot."},
                {"role":"user", "content":chat_content}]

    outputs = []
    for m in MODELS:
        output = m.complete_chat(messages)
        outputs.append({"model":str(m), "content":output})

    return {"status":"ok", "outputs":outputs}

@APP.route('/')
def index():
    """
    Displays the index page accessible at '/'
    """
    return render_template('index.html')

def run():
    """
    Launches a local web server for interfacing with PhaseLLM. This is meant to be for testing purposes only.
    """
    APP.run()