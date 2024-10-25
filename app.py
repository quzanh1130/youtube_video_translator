import os
import base64
import tempfile
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from transcriber import Transcriber  # Import the Transcriber class

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('audio_data')
def handle_audio(data):
    # Decode base64 audio data
    audio_data = base64.b64decode(data)

    # Save audio data to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio_file:
        temp_audio_file.write(audio_data)
        temp_audio_file_path = temp_audio_file.name

    # Transcribe audio using the Transcriber class
    try:
        transcriber = Transcriber(temp_audio_file_path)
        segments, language = transcriber.transcribe_audio()
        transcript = " ".join([segment['text'] for segment in segments])
    except ValueError as e:
        transcript = str(e)

    # Remove the temporary file
    os.remove(temp_audio_file_path)

    emit('transcript', {'text': transcript})

if __name__ == '__main__':
    socketio.run(app, debug=True)
