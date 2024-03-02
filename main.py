from flask import Flask, render_template, redirect, url_for
import random
import string
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

app = Flask(__name__)

# Dictionary to store rooms and their corresponding codes
rooms = {}

# Function to generate a random 6-digit code
def generate_room_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_room')
def create_room():
    room_code = generate_room_code()
    rooms[room_code] = []
    return redirect(url_for('room', room_code=room_code))

@app.route('/room/<string:room_code>')
def room(room_code):
    if room_code in rooms:
        return render_template('room.html', room_code=room_code)
    else:
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)