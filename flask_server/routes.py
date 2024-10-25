import os
from flask import jsonify, request, send_file
import json
from werkzeug.utils import secure_filename
from config import Config

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')


def register_routes(app):
    # Ensure upload directory exists
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    @app.route('/api/v2/get/data', methods=['GET'])
    def get_json_data():
        """Serves the JSON data from a file."""
        file_path = os.path.join(UPLOAD_FOLDER,Config.JSON_FILE)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            return jsonify({"error": "No data available"}), 404

    @app.route('/api/v2/add/data', methods=['POST'])
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
