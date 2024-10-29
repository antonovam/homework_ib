import os
import json
from flask import Blueprint, jsonify, request, send_file
from werkzeug.utils import secure_filename
from flask_server.config import Config

# Define the Blueprint for API version v2
v2 = Blueprint('v2', __name__)

# Set the upload directory path
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../uploads')

# Ensure upload directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@v2.route('/get/data', methods=['GET'])
def get_json_data():
    """Serves the JSON data from a file."""
    file_path = os.path.join(UPLOAD_FOLDER, Config.JSON_FILE)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return jsonify({"error": "No data available"}), 404


@v2.route('/add/data', methods=['POST'])
def add_json_data():
    """Handles JSON data upload via direct POST or file attachment."""
    if 'file' in request.files:
        file = request.files['file']
        if file.filename.endswith('.json'):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            return jsonify({"message": "File uploaded successfully"}), 200
    elif request.is_json:
        json_data = request.get_json()
        file_path = os.path.join(UPLOAD_FOLDER, Config.JSON_FILE)
        with open(file_path, 'w') as f:
            json.dump(json_data, f)
        return jsonify({"message": "JSON data saved successfully"}), 200
    return jsonify({"error": "Invalid data format"}), 400
