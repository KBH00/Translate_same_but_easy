from app import app
from flask import request, jsonify, render_template
import os
from werkzeug.utils import secure_filename
from threading import Lock
from .pre_processing import ocr_paddle, extract_text_from_pdf  # Assuming pre_processing.py is in the root directory

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_IMG = {'png', 'jpg', 'jpeg'}
ALLOWED_PDF = {'pdf'}
process_lock = Lock()

def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

@app.route('/')
def home():
    print("Current working directory:", os.getcwd())
    print("Templates directory absolute path:", os.path.abspath('templates'))
    return render_template('test.html')

@app.route('/text', methods=['POST'])
def analyze_text():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    if not process_lock.acquire(False):
        return jsonify({'error': 'Another request is being processed. Please wait.'}), 429
    try:
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file_extension = filename.rsplit('.', 1)[1].lower()
            
            if allowed_file(filename, ALLOWED_PDF):
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                try:
                    text = extract_text_from_pdf(file_path)
                    return jsonify({'text': text})
                finally:
                    os.remove(file_path)
            
            elif allowed_file(filename, ALLOWED_IMG):
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                try:
                    text = ocr_paddle(file_path)
                    return jsonify({'text': text})
                finally:
                    os.remove(file_path)
    
        else:
            return jsonify({'error': 'Invalid file type or file not uploaded properly'}), 400
    finally:
        process_lock.release()
