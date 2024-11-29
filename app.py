from flask import Flask, request, jsonify, send_file
import json
import os
import pandas as pd

app = Flask(__name__)

# File to store responses
DATA_FILE = 'responses.json'

# Load existing data from the JSON file or create an empty list if the file doesn't exist
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'r') as file:
        responses = json.load(file)
else:
    responses = []

@app.route('/submit', methods=['POST'])
def submit():
    """
    Endpoint to receive and save form responses.
    """
    global responses
    # Parse JSON data from the request
    data = request.json
    responses.append(data)

    # Save updated responses back to the file
    with open(DATA_FILE, 'w') as file:
        json.dump(responses, file, indent=4)

    return jsonify({'message': 'Response saved successfully!'}), 200

@app.route('/download', methods=['GET'])
def download():
    """
    Endpoint to generate and serve the Excel file.
    """
    global responses
    # Convert the responses to a DataFrame
    df = pd.DataFrame(responses)
    file_path = 'Air_Carbon_Project_Responses.xlsx'
    # Save the DataFrame to an Excel file
    df.to_excel(file_path, index=False)

    # Serve the file for download
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    # Run the Flask server
    app.run(debug=True)
