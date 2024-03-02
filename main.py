from flask import Flask, render_template, redirect, url_for, request, session
import random
import string
import re
import google.generativeai as genai


gemini_api = "AIzaSyAICX1lE8ap5Ee_XnZfmLH1azaNKuzVrFQ"
genai.configure(api_key=gemini_api)

model = genai.GenerativeModel('gemini-1.0-pro')

def generate_question():
    chat = model.start_chat(history=[])
    response = chat.send_message(f"give me an ice breaker question")

    return re.sub(r"\*|\"", "", response.text)

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Dictionary to store rooms
rooms = {}

# Function to generate a random 6-digit code
def generate_room_code():
    while True:
        room_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        if room_code not in rooms:
            return room_code

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_room', methods=['POST'])
def create_room():
    player_name = request.form['player_name']
    room_code = generate_room_code()
    session['player_name'] = player_name
    rooms[room_code] = [player_name]
    return redirect(url_for('room', room_code=room_code))

@app.route('/join_room', methods=['POST'])
def join_room():
    room_code = request.form['room_code']
    player_name = request.form['player_name']

    session['player_name'] = player_name
    
    if room_code in rooms:
        rooms[room_code].append(player_name)
    else:
        rooms[room_code] = [player_name]
    
    return redirect(url_for('room', room_code=room_code))

@app.route('/room/<string:room_code>')
def room(room_code):
    if room_code in rooms:
        players = rooms[room_code]
        current_player = session.get('player_name')
        return render_template('room.html', room_code=room_code, players=players, current_player=current_player)
    else:
        return redirect(url_for('index'))


@app.route('/generate_text', methods=['POST'])
def generate_text_route():
    text = generate_question()
    return text

if __name__ == '__main__':
    app.run(debug=True)