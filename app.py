from flask import Flask, request, jsonify
from PIL import Image
import pytesseract
import os

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.jpeg', '.png']
app.config['UPLOAD_FOLDER'] = '/tmp'

@app.route('/ocr', methods=['POST'])
def ocr():
    if 'file' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Empty filename'}), 400

    try:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        image = Image.open(filepath)
        text = pytesseract.image_to_string(image)

        return jsonify({'text': text}), 200

    except Exception as e:
        return jsonify({'error': 'Processing failed', 'details': str(e)}), 500

@app.route('/', methods=['GET'])
def index():
    return 'Tesseract OCR API is running.'

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
