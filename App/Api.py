from flask import Blueprint, request, jsonify, send_file
import os
from visuals import generate_visualizations_from_file

api = Blueprint('api', __name__)

@api.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    if file:
        upload_folder = 'uploads'
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, file.filename)
        file.save(file_path)
        visualizations = generate_visualizations_from_file(file_path)
        return jsonify(visualizations)

@api.route('/visualization/<filename>', methods=['GET'])
def get_visualization():
    filename = request.args.get('filename')
    file_path = os.path.join('uploads', filename)
    if os.path.exists(file_path):
        return send_file(file_path, mimetype='image/svg+xml')
    else:
        return "File not found", 404
