import flask
import re
from dotenv import dotenv_values
import pathlib
import textwrap

import google.generativeai as genai


config = dotenv_values(".env")
gemini_api = config["gemini_api"]
genai.configure(api_key=gemini_api)

model = genai.GenerativeModel('gemini-1.0-pro')

def generate_question(num_of_player):
    chat = model.start_chat(history=[])
    response = chat.send_message(f"give me an ice breaker question for {num_of_player} people")
    return re.sub(r"\*|\"", "", response.text)



for i in range(5, 10):
    print(generate_question(i))

