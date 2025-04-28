import os
import uuid
import json
from flask import Flask, request, redirect, url_for, render_template, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from utils import convert_mp3_to_wav, transcribe_audio
from datetime import datetime
from pydub.utils import mediainfo
from models import db, File
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///files.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)


with app.app_context():
    db.create_all()

history_file = 'history.json'

def load_history():
    if os.path.exists(history_file):
        with open(history_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_history(data):
    with open(history_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

app = Flask(__name__)
recent_files = load_history()
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

        info = mediainfo(filepath)
        duration_sec = float(info['duration']) if 'duration' in info else 0
        
        task_id = str(uuid.uuid4())
        tasks[task_id] = {
            'status': 'processing',
            'step': 'Starting conversion...',
            'filename': filename,
            'text': ''
        }
        recent_files.append({
        'name': filename,
        'uploaded': datetime.now().strftime("%d %b %Y %H:%M"),
        'duration': duration_sec,
        'mode': 'Vosk offline',
        'status': 'Processing'})

        save_history(recent_files)

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


@app.route('/recent')
def recent():
    recent_files = load_history()
    return render_template('recent.html', files=recent_files)


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/admin/files')
def admin_files():
    files = File.query.order_by(File.uploaded.desc()).all()
    return render_template('admin_files.html', files=files)

# Редактирование файла
@app.route('/admin/files/edit/<int:file_id>', methods=['GET', 'POST'])
def edit_file(file_id):
    file = File.query.get_or_404(file_id)
    if request.method == 'POST':
        file.status = request.form.get('status')
        file.mode = request.form.get('mode')
        db.session.commit()
        return redirect(url_for('admin_files'))
    return render_template('edit_file.html', file=file)

# Удаление файла
@app.route('/admin/files/mass-delete', methods=['POST'])
def mass_delete_files():
    ids = request.form.getlist('file_ids')
    if ids:
        for file_id in ids:
            file = File.query.get(file_id)
            if file:
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.name)
                if os.path.exists(filepath):
                    os.remove(filepath)  # <-- удаляем физический mp3-файл из uploads/
                db.session.delete(file)  # <-- удаляем запись из базы
        db.session.commit()
    return redirect(url_for('admin_files'))



if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['RESULT_FOLDER'], exist_ok=True)
    app.run(debug=True)
