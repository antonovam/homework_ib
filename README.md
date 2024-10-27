# Flask Client-Server Project

## Project Overview

This project is a Flask-based client-server application designed to handle JSON data parsing, storage, and retrieval. The application provides a RESTful API for uploading and retrieving JSON files, as well as a command-line interface for managing data. All data is stored in a local SQLite database using SQLAlchemy ORM.

### **Features**
- **Flask Server** with REST API:
  - **POST**: Upload JSON data or a JSON file.
  - **GET**: Retrieves JSON file.
- **Flask Client** with Command-Line Interface (CLI):
  - **Fetch and store JSON data** from the server.
  - **Send JSON data** or upload JSON files to the server.
- **Data Parsing and Storage**:
  - Parses complex JSON structures following given example (exanple.json).
  - Stores parsed data into an SQLite database.
- **Automated Tests**:
  - Tests for GET/POST requests.
  - Tests for data parsing accuracy.
  - Database CRUD operations validation.

## Installation

### **Requirements**
Make sure you have **Python 3.8+** installed. All dependencies are listed in `requirements.txt`.

### **Step-by-Step Guide**

1. **Clone the repository**:
   ```bash
   git clone https://github.com/antonovam/homework_ib.git
   cd homework_ib
    ```
2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  
    ```
3.  **Install dependencies**:
   ```bash
   pip install -r requirements.txt
```
## **Running the Application**

1. **Start the Flask Server**: 

Make sure you are in the root directory of the project
   ```bash
   python server.py
  ```

The server will start on ```localhost:5001```. You should see output indicating that the server is running.

2. **Running the Client**:

To interact with the server via the client, use the following commands:

**Upload Data**

- **Post JSON Data**

```bash
python client.py post
```

- **Post JSON File**

```bash
python client.py post --file example.json
```
**Fetch and Store Data**

```bash
python client.py get
```

## Running Tests
 

Make sure you are in the root directory of the project
```bash
pytest tests
```

