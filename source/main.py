import os
import re
import requests
from flask import Flask, render_template, request


try:
    FILE_MIN_SIZE = int(os.environ['FILE_MIN_SIZE'])
except KeyError:
    FILE_MIN_SIZE = 0

try:
    SERVER_PAIR = os.environ['SERVER_PAIR']
    if "http://" not in SERVER_PAIR:
        SERVER_PAIR = "http://" + SERVER_PAIR
except KeyError:
    SERVER_PAIR = None

try:
    ALLOWED_CHARS = os.environ['ALLOWED_CHARS']
except KeyError:
    ALLOWED_CHARS = '^[a-zA-Z0-9\-\_\.]+$'


LISTEN_PORT = 80
PARENT_DIRECTORY = '/data'

UPLOAD_SUCCESS_MESSAGE = """
    <h3 style="color: #008000;">
    File successfully uploaded!
    </h3>
    """

UPLOAD_FAIL_MESSAGE = """
    <h3 style="color: #C04000;">
    File failed to upload due to inappropriate characters \
    in file/directory names
    </h3>
    """

FILE_EXISTS_MESSAGE = """
    <h3 style="color: #C04000;">
    File already exists
    </h3>
    """

EMPTY_FILE_MESSAGE = f"""
    <h3 style="color: #C04000;">
    The size of the uploaded file is equal to or less \
    than {FILE_MIN_SIZE} bytes
    </h3>
    """


def parse_names(name):
    if re.search(ALLOWED_CHARS, name):
        return True
    else:
        return False


def validate_file_size(file):
    file.seek(0, 2)
    file_length = file.tell()
    file.stream.seek(0)
    if file_length > FILE_MIN_SIZE:
        return True
    else:
        return False


def send_file(file, upload_dir_name):
    full_dir_name = os.path.join(PARENT_DIRECTORY, upload_dir_name)
    data = {'directory_field': f'{upload_dir_name}', 'resend': 'True'}
    files = {'upload_file': open(f'{full_dir_name}/{file.filename}', 'rb')}
    file_post_request = requests.post(SERVER_PAIR, data=data, files=files)


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('upload.html')


@app.route('/', methods=['POST'])
def my_form_post():

    upload_dir_name = request.form['directory_field']

    validate_dir_name = parse_names(upload_dir_name)
    if validate_dir_name is False:
        return(UPLOAD_FAIL_MESSAGE + render_template('upload.html'))

    full_dir_name = os.path.join(PARENT_DIRECTORY, upload_dir_name)

    file = request.files['upload_file']

    if validate_file_size(file) is False:
        return(EMPTY_FILE_MESSAGE + render_template('upload.html'))

    validate_file_name = parse_names(file.filename)
    if validate_file_name is True:
        full_file_path = os.path.join(PARENT_DIRECTORY, upload_dir_name,
            file.filename)
    else:
        return(UPLOAD_FAIL_MESSAGE + render_template('upload.html'))

    if os.path.isfile(full_file_path):
        return (FILE_EXISTS_MESSAGE + render_template('upload.html'))
    else:
        if not os.path.exists(full_dir_name):
            os.makedirs(full_dir_name)
        file.save(full_file_path)
        if SERVER_PAIR and request.form.get('resend') is None:
            send_file(file, upload_dir_name)

    return(UPLOAD_SUCCESS_MESSAGE + render_template('upload.html'))


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=80)
