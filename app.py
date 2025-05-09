# Description: This is the main file for the Flask application. It contains the routes for the API.

from flask import Flask, jsonify, request
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Define a pasta onde as imagens serão salvas
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Garante que a pasta existe
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Test route
@app.route('/')
def hello_world():
    return 'Hello, World!'

# Photo upload route
@app.route('/image_upload', methods=['POST'])
def photo_upload():
    try:
        image_file = request.files["image"]

        # Define o caminho completo para salvar a imagem
        image_path = os.path.join(app.config["UPLOAD_FOLDER"], image_file.filename)
        image_file.save(image_path)

        return jsonify({'message': 'Photo uploaded successfully!'})
    
    except Exception as e:
        return jsonify({'message': 'Error uploading photo!'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)