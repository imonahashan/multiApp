import os
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import speech_recognition as sr
import googletrans
from pdf2docx import Converter


app = Flask(__name__)

UPLOAD_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('index.html',user_name='Imon')


@app.route("/about")
def about_page():
    skills = [
        {'id': 1, 'skill_name': 'HTML', 'points': 80},
        {'id': 2, 'skill_name': 'CSS', 'points': 90},
        {'id': 3, 'skill_name': 'javaScript', 'points': 75},
        {'id': 4, 'skill_name': 'SQL', 'points': 95},
        {'id': 5, 'skill_name': 'PL/SQL', 'points': 95},
        {'id': 6, 'skill_name': 'Oracle Apex', 'points': 85}
    ]
    return render_template('about.html', user_name='Imon',skills=skills)

@app.route("/translate")
def translate_page():
    return render_template('translate.html')


@app.route("/speech2text")
def speech2text():
    return render_template('speech2text.html')

# Route to process the audio
@app.route('/convert', methods=['POST'])
def convert_speech_to_text():
    if 'audio_data' not in request.files:
        return jsonify({'error': 'No file part'})

    audio_file = request.files['audio_data']

    # Save the received audio to a temporary file
    temp_audio_path = 'voice_ahashan.wav'
    audio_file.save(temp_audio_path)

    # Get the selected language from the form data
    selected_language = request.form.get('language', 'en')  # Default to English if not provided

    # Perform speech-to-text conversion
    recognizer = sr.Recognizer()
    with sr.AudioFile(temp_audio_path) as source:
        audio_text = recognizer.recognize_google(audio_data=source)
        print(audio_text)
    # Delete the temporary audio file
    os.remove(temp_audio_path)

    translator = googletrans.Translator()
    translated_text = translator.translate(audio_text, dest=selected_language)

    return jsonify({'text': audio_text, 'translated_text': translated_text})

@app.route("/pdf2dox")
def pdf2dox():
    return render_template('pdf2dox.html')


@app.route('/pdf_convert', methods=['POST'])
def pdf_convert():
    if 'pdf_file' not in request.files:
        return "No file part"

    pdf_file = request.files['pdf_file']

    if pdf_file.filename == '':
        return "No selected file"

    # Convert PDF to Word
    pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_file.filename)
    pdf_file.save(pdf_path)

    docx_file = os.path.splitext(pdf_file.filename)[0] + '.docx'
    docx_path = os.path.join('converted', docx_file)

    cv = Converter(pdf_path)
    cv.convert(docx_path)
    cv.close()
    os.remove(pdf_path)

    return send_file(docx_path, as_attachment=True, download_name=docx_file)

@app.route("/audioRecorder")
def audioRecorder():
    return render_template('audioRecorder.html')


if __name__ == '__main__':
    app.run(debug=True)
