import os
import uuid
from flask import Flask, request, redirect, url_for, render_template, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from utils import convert_mp3_to_wav, transcribe_audio

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['RESULT_FOLDER'] = 'results'

tasks = {}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'mp3'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        task_id = str(uuid.uuid4())
        tasks[task_id] = {
            'status': 'processing',
            'step': 'Starting conversion...',
            'filename': filename,
            'text': ''
        }

        process_file(task_id, filepath)

        return jsonify({'task_id': task_id})
    return jsonify({'error': 'Invalid file type'}), 400

def process_file(task_id, filepath):
    tasks[task_id]['step'] = 'Converting MP3 to WAV...'
    wav_filepath = convert_mp3_to_wav(filepath)

    if not wav_filepath:
        tasks[task_id]['status'] = 'error'
        tasks[task_id]['step'] = 'Failed to convert file.'
        return

    tasks[task_id]['step'] = 'Recognizing speech...'
    text_data = transcribe_audio(wav_filepath)
    if text_data:
        tasks[task_id]['status'] = 'completed'
        tasks[task_id]['text'] = text_data
    else:
        tasks[task_id]['status'] = 'error'
        tasks[task_id]['step'] = 'Speech recognition failed.'

@app.route('/status/<task_id>')
def task_status(task_id):
    task = tasks.get(task_id)
    if not task:
        return jsonify({'status': 'error', 'step': 'Task not found.'}), 404
    return jsonify({
        'status': task['status'],
        'step': task.get('step', 'Processing...')
    })

@app.route('/result/<task_id>')
def task_result(task_id):
    task = tasks.get(task_id)
    if not task or task['status'] != 'completed':
        return redirect(url_for('index'))
    return render_template('result.html', filename=task['filename'], words=task['text'])

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['RESULT_FOLDER'], exist_ok=True)
    app.run(debug=True)
