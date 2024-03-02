from flask import Flask, render_template, redirect, url_for
import random
import string

app = Flask(__name__)

# Dictionary to store rooms and their corresponding codes
rooms = {}

# Function to generate a random 6-digit code
def generate_room_code():
    while True:
        room_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        if room_code not in rooms:
            rooms.add(room_code)
            return room_code

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