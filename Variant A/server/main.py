import env_storage
from flask import Flask, jsonify, request, send_file, Response, redirect, render_template
import os
from flask_cors import CORS
# from flask_jwt_extended import JWTManager
import socket
app = Flask(__name__)
# app.config['JWT_SECRET_KEY'] = os.environ.get("JWT_SECRET")

# Configure JWT settings
# jwt = JWTManager(app)
CORS(app, expose_headers=['File-Type'])

SHARED_ROOT_DIRECTORY = os.path.join(
    os.getcwd(), 'server', os.environ.get('SHARED_DATA_FOLDER_NAME'))


@app.route('/')
def home():
    # return redirect("http://127.0.0.1:7000", code=301)
    return render_template("index.html")


@app.route('/get_local_ip', methods=['GET'])
def get_local_ip():
    ip_address = socket.gethostbyname(socket.gethostname())
    return jsonify({'ip': ip_address})


@app.route('/file', methods=['POST', 'PUT', 'GET', 'DELETE'])
def upload_file():
    if request.method == 'POST':
        print("Get File", request.json['filename'])
        try:
            file_path = os.path.join(
                SHARED_ROOT_DIRECTORY, request.json['filename'])

            # Check if the file was found
            if file_path:
                # Check if the file exists
                if os.path.isfile(file_path):
                    # return send_file(file_path)
                    # Read the file into a Blob
                    with open(file_path, 'rb') as file:
                        file_blob = file.read()

                    # Get the file extension from the filename
                    file_extension = os.path.splitext(
                        request.json['filename'])[-1]

                    # Create a Response object with the file Blob
                    response = Response(
                        file_blob, content_type='application/octet-stream')

                    # Set the Content-Disposition header with the filename
                    temp = request.json['filename']
                    response.headers['Content-Disposition'] = f'attachment; filename={temp}'

                    # Set the file_type response header with the file extension
                    response.headers['File-Type'] = file_extension

                    return response
            else:
                return "File not found", 404
        except Exception as e:
            return str(e)
    if request.method == 'PUT':
        try:
            uploaded_files = request.files.getlist('file')
            print("Uploaded files ------------------------------->", request.files)
            for file in uploaded_files:
                if file.filename == '':
                    return "No file selected", 400
                if file.filename in os.listdir(SHARED_ROOT_DIRECTORY):
                    print("File already exists : ", file.filename)
                file.save(os.path.join(SHARED_ROOT_DIRECTORY, file.filename))

            return jsonify({"message": "File(s) uploaded successfully"}), 200
        except Exception as e:
            return str(e), 500
    elif request.method == 'DELETE':
        try:
            target = os.path.join(SHARED_ROOT_DIRECTORY,
                                  request.json['filename'])

            if os.path.exists(target):
                os.remove(target)
                return jsonify({"message": "File removed successfully"}), 200
        except Exception as e:
            return str(e), 500


@app.route('/all-files', methods=['GET'])
def list_all_files():
    try:
        items = os.listdir(SHARED_ROOT_DIRECTORY)

        # Separate files and folders
        files = [item for item in items if os.path.isfile(
            os.path.join(SHARED_ROOT_DIRECTORY, item))]

        # Create a list of dictionaries with filename and size in MB
        file_info_list = []
        for filename in files:
            file_path = os.path.join(SHARED_ROOT_DIRECTORY, filename)
            size_in_bytes = os.path.getsize(file_path)
            size_in_mb = size_in_bytes / (1024 * 1024)  # Convert to MB
            file_info = {
                'filename': filename,
                'size_mb': size_in_mb
            }
            file_info_list.append(file_info)

        # Return the list as JSON response
        return jsonify(file_info_list), 200
    except Exception as e:
        return str(e), 500


if __name__ == '__main__':
    app.run(debug=True, port=7001, host='0.0.0.0')
