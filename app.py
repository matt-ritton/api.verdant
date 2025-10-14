# Description: This is the main file for the Flask application. It contains the routes for the API.

import json
from flask import Flask, jsonify, request
from flask_cors import CORS
import os

from resources.model import predict

app = Flask(__name__)
CORS(app)

# Upload folder configuration
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Make sure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Test route
@app.route('/')
def hello_world():
    return 'Hello, World!'

# Route to get the list of phytopathologies
@app.route('/get_dictionary', methods=['GET'])
def get_dictionary():
    try:
        # Load the JSON file containing the class names
        with open("./resources/data/dictionary.pt.json", "r", encoding="utf-8") as f:
            labels = json.load(f)
        
        return jsonify(labels), 200
    
    except Exception as e:
        return jsonify({'message': 'Error loading phytopathologies!'}), 500

# Photo upload route
@app.route('/image_upload', methods=['POST'])
def photo_upload():
    try:
        image_file = request.files["image"]

        # Define o caminho completo para salvar a imagem
        image_path = os.path.join(app.config["UPLOAD_FOLDER"], image_file.filename)
        image_file.save(image_path)

        # Call the prediction function
        predicted_class = predict(image_path)

        # Remove the image after prediction
        os.remove(image_path)

        return jsonify({'message': predicted_class}), 200
    
    except Exception as e:
        return jsonify({'message': 'Error uploading photo!'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)