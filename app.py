from flask import Flask, request, send_file, render_template_string
import torch
from TTS.api import TTS
import os

app = Flask(__name__)

device = "cuda" if torch.cuda.is_available() else "cpu"

def generate_audio(text="A journey of a thousand miles begins with a single step."):
    tts = TTS(model_name='tts_models/en/ljspeech/fast_pitch').to(device)
    output_path = "outputs/output.wav"
    tts.tts_to_file(text=text, file_path=output_path)
    return output_path

@app.route('/')
def index():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Text to Audio</title>
    </head>
    <body>
        <h1>Text to Audio</h1>
        <form action="/generate-audio" method="post">
            <label for="text">Enter text:</label>
            <input type="text" id="text" name="text" required>
            <button type="submit">Generate Audio</button>
        </form>
        {% if audio_url %}
        <audio controls>
            <source src="{{ audio_url }}" type="audio/wav">
            Your browser does not support the audio element.
        </audio>
        {% endif %}
    </body>
    </html>
    ''')

@app.route('/generate-audio', methods=['POST'])
def generate_audio_route():
    text = request.form['text']
    output_path = generate_audio(text)
    return send_file(output_path, as_attachment=True)

if __name__ == "__main__":
    os.makedirs('outputs', exist_ok=True)
    app.run(debug=True)