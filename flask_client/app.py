from flask import Flask, jsonify, request
from config import Config
from services import get_json_data, send_post_data
from parser import DataParser
from models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
app.config.from_object(Config)

# Database setup
engine = create_engine(app.config['DATABASE_URL'])
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


# Route to fetch and store data from the server
@app.route('/fetch-and-store', methods=['GET'])
def fetch_and_store_data():
    server_url = f"{app.config['SERVER_URL']}/api/v2/get/data"

    # Fetch data from the server
    json_data = get_json_data(server_url)
    if not json_data:
        return jsonify({"error": "Failed to fetch data from the server"}), 500

    # Parse and store the JSON data in the database
    parser = DataParser(json_data)
    session = Session()
    try:
        parser.save_to_database(session)
        return jsonify({"status": "Data fetched and stored successfully"}), 200
    except Exception as e:
        session.rollback()
        return jsonify({"error": f"Failed to store data: {e}"}), 500
    finally:
        session.close()


# Route to upload JSON data or a file to the server
@app.route('/upload-data', methods=['POST'])
def upload_data():
    if 'file' in request.files:
        file = request.files['file']
        server_url = f"{app.config['SERVER_URL']}/api/v2/add/data"
        status_code, response = send_post_data(server_url, file=file.filename)
    else:
        json_data = {"key": "value"}  # Example data
        server_url = f"{app.config['SERVER_URL']}/api/v2/add/data"
        status_code, response = send_post_data(server_url, data=json_data)

    if status_code == 200:
        return jsonify({"status": "POST request successful", "response": response}), 200
    else:
        return jsonify({"error": "Failed to upload data"}), 500


if __name__ == '__main__':
    app.run(port=5002)
