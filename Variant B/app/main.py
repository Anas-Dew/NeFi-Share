from flask import Flask, jsonify, request, Response, render_template
from flask_cors import CORS
import os
import socket
import env_storage
import signal
import sys
import atexit
from plyer import notification
app = Flask(__name__, template_folder="templates")
CORS(app, expose_headers=['File-Type'])
SHARED_ROOT_DIRECTORY = os.path.join(
    os.getcwd(), os.environ.get('SHARED_DATA_FOLDER_NAME'))
if not os.path.exists(SHARED_ROOT_DIRECTORY):
        os.makedirs(SHARED_ROOT_DIRECTORY)

@app.route('/')
def home():
    return render_template("index.html")


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404


@app.route('/get_local_ip', methods=['GET'])
def get_local_ip():
    ip_address = socket.gethostbyname(socket.gethostname())
    return jsonify({'ip': ip_address})


@app.route('/file', methods=['POST', 'PUT', 'DELETE'])
def file_operations():
    if request.method == 'POST':
        filename = request.get_json()['filename']
        return send_file_from_directory(filename)

    if request.method == 'PUT':
        uploaded_files = request.files.getlist('file')
        return store_files(uploaded_files)

    if request.method == 'DELETE':
        filename = request.get_json()['filename']
        return delete_file(filename)


def send_file_from_directory(filename):
    try:
        file_path = os.path.join(SHARED_ROOT_DIRECTORY, filename)
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as file:
                file_blob = file.read()

            file_extension = os.path.splitext(filename)[-1]

            response = Response(
                file_blob, content_type='application/octet-stream')
            response.headers['Content-Disposition'] = f'attachment; filename={filename}'
            response.headers['File-Type'] = file_extension

            return response
        else:
            return "File not found", 404

    except Exception as e:
        return str(e)


def store_files(uploaded_files):
    try:
        for file in uploaded_files:
            if file.filename == '':
                return "No file selected", 400
            if file.filename in os.listdir(SHARED_ROOT_DIRECTORY):
                print("File already exists : ", file.filename)
            file.save(os.path.join(SHARED_ROOT_DIRECTORY, file.filename))

        return jsonify({"message": "File(s) uploaded successfully"}), 200
    except Exception as e:
        return str(e), 500


def delete_file(filename):
    try:
        target = os.path.join(SHARED_ROOT_DIRECTORY, filename)

        if os.path.exists(target):
            os.remove(target)
            return jsonify({"message": "File removed successfully"}), 200
    except Exception as e:
        return str(e), 500


@app.route('/all-files', methods=['GET'])
def list_all_files():
    try:
        items = [item for item in os.listdir(SHARED_ROOT_DIRECTORY) if os.path.isfile(
            os.path.join(SHARED_ROOT_DIRECTORY, item))]

        # Create a list of dictionaries with filename and size in MB
        file_info_list = [{
            'filename': filename,
            # Convert to MB
            'size_mb': os.path.getsize(os.path.join(SHARED_ROOT_DIRECTORY, filename)) / (1024 * 1024)
        } for filename in items]

        return jsonify(file_info_list), 200
    except Exception as e:
        return str(e), 500


# ------------------------
def exit_handler():
    notification.notify(
        title="System Message",
        message="Thank you for using",
        timeout=10
    )
    print("Thank you for using")


# Register the exit_handler to be called when the script is terminated
atexit.register(exit_handler)

# Define a signal handler for SIGTERM


def sigterm_handler(signum, frame):
    print("Caught SIGTERM signal")
    exit_handler()
    sys.exit(0)


# Register the sigterm_handler for SIGTERM signal
signal.signal(signal.SIGTERM, sigterm_handler)


if __name__ == '__main__':
    app.run(debug=True, port=7000, host='0.0.0.0')
