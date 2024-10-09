from flask import Flask, render_template, request, redirect, url_for
import cv2
from PIL import Image
import easyocr
import numpy as np
import json
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

class ImageAnnotator:
    def __init__(self, image_path):
        self.load_image(image_path)
        self.keys_texts = {}

    def load_image(self, image_path):
        self.image = cv2.imread(image_path)
        self.image_rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        self.image_pil = Image.fromarray(self.image_rgb)

    def add_annotation(self, key, x1, y1, x2, y2):
        self.keys_texts[key] = (x1, y1, x2, y2)

    def extract_texts(self):
        reader = easyocr.Reader(['en'])
        texts = {}
        for key, (x1, y1, x2, y2) in self.keys_texts.items():
            image_array = np.array(self.image_pil)
            cropped_image = image_array[y1:y2, x1:x2]
            results = reader.readtext(cropped_image)
            extracted_text = ' '.join([text for (_, text, _) in results])
            texts[key] = extracted_text
        return texts

    def save_texts_to_json(self, texts, filename):
        with open(filename, 'w') as json_file:
            json.dump(texts, json_file, indent=4)

    def save_form_data(self, filename):
        with open(filename, 'w') as json_file:
            json.dump(self.keys_texts, json_file, indent=4)

    def load_form_data(self, filename):
        with open(filename, 'r') as json_file:
            self.keys_texts = json.load(json_file)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        return redirect(url_for('annotate', filename=file.filename))
    return redirect(request.url)

@app.route('/annotate/<filename>', methods=['GET', 'POST'])
def annotate(filename):
    if request.method == 'POST':
        key = request.form['key']
        x1, y1, x2, y2 = map(int, request.form['coords'].split(','))
        annotator = ImageAnnotator(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        annotator.add_annotation(key, x1, y1, x2, y2)
        annotator.save_form_data(os.path.join(app.config['UPLOAD_FOLDER'], 'form_data.json'))
        return redirect(url_for('extract_texts', filename=filename))
    return render_template('annotate.html', filename=filename)

@app.route('/extract/<filename>')
def extract_texts(filename):
    annotator = ImageAnnotator(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    annotator.load_form_data(os.path.join(app.config['UPLOAD_FOLDER'], 'form_data.json'))
    texts = annotator.extract_texts()
    annotator.save_texts_to_json(texts, os.path.join(app.config['UPLOAD_FOLDER'], 'extracted_texts.json'))
    return render_template('extract.html', texts=texts)

if __name__ == '__main__':
    app.run(debug=True)
