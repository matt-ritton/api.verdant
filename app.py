# Description: This is the main file for the Flask application. It contains the routes for the API.

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

# Photo upload route
@app.route('/image_upload', methods=['POST'])
def photo_upload():
    try:
        image_file = request.files["image"]

        # Define o caminho completo para salvar a imagem
        image_path = os.path.join(app.config["UPLOAD_FOLDER"], image_file.filename)
        image_file.save(image_path)

        predicted_class = predict(image_path)  # Call the prediction function

        # Remove the image after prediction
        os.remove(image_path)

        return jsonify({'message': 'Predicted class: ' + predicted_class})
    
    except Exception as e:
        return jsonify({'message': 'Error uploading photo!'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)