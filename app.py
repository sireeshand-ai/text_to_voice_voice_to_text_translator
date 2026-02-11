
from flask import Flask, render_template, request, jsonify, send_file
from googletrans import Translator
from gtts import gTTS
import time

app = Flask(__name__)
translator = Translator()

last_audio = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    text = request.form['text']
    src = request.form['input_lang']
    dest = request.form['output_lang']

    translated = translator.translate(text, src=src, dest=dest)
    return translated.text

@app.route('/speak', methods=['POST'])
def speak():
    global last_audio
    text = request.form['text']
    lang = request.form['lang']

    filename = f"output_{int(time.time())}.mp3"
    tts = gTTS(text=text, lang=lang)
    tts.save(filename)
    last_audio = filename

    return filename

@app.route('/audio/<filename>')
def audio(filename):
    return send_file(filename)

if __name__ == '__main__':
    app.run(debug=True)
