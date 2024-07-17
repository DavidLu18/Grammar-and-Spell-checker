from flask import Flask, request, render_template
import os
from werkzeug.utils import secure_filename
import docx
import pandas as pd
from grammar_checker import GrammarChecker

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'docx'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
checker = GrammarChecker('en-US')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def read_file_content(filepath):
    if filepath.endswith('.docx'):
        doc = docx.Document(filepath)
        content = "\n".join([para.text for para in doc.paragraphs])
    elif filepath.endswith('.txt'):
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
    else:
        content = ""
    return content

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check():
    text = request.form['text']
    matches = checker.check_grammar(text)
    corrections = []
    for match in matches:
        corrections.append({
            'offset': match.offset,
            'errorLength': match.errorLength,
            'message': match.message,
            'replacements': match.replacements
        })
    return render_template('result.html', text=text, corrections=corrections)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        content = read_file_content(filepath)
        matches = checker.check_grammar(content)
        corrections = []
        for match in matches:
            corrections.append({
                'offset': match.offset,
                'errorLength': match.errorLength,
                'message': match.message,
                'replacements': match.replacements
            })
        return render_template('result.html', text=content, corrections=corrections)
    else:
        return 'File not allowed'

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
