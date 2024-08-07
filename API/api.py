from Utilities.FileEncryptor import FileEncryptor
from Handler.PartitionManager import PartitionManager, PartitionFinder
from Utilities.BytesConverter import BytesManager
from Handler.cfgHandler import ConfigHandler
from Handler.DBHandler import UserDatabase
import shutil
import tempfile
from flask import Flask, redirect, url_for, session, request, jsonify, send_file, after_this_request
from flask_restful import Resource, abort, Api
from flask_sqlalchemy import SQLAlchemy
from flask_oauthlib.client import OAuth  # type: ignore
import os
import binascii
from datetime import datetime
from functools import wraps
from werkzeug.utils import secure_filename
import time
import logging

from dotenv import load_dotenv  # type: ignore
load_dotenv()


LOGGING_ENABLED = True

# Setup logging
if not os.path.exists('logs'):
    os.makedirs('logs')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log') if LOGGING_ENABLED else logging.NullHandler(),
        logging.StreamHandler() if LOGGING_ENABLED else logging.NullHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///oauth_tokens.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.abspath(
    os.path.join(os.getcwd(), 'uploads'))  # Ensure absolute path
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Maximum file size: 16MB

api = Api(app)
db = SQLAlchemy(app)
oauth = OAuth(app)

# Initialize UserDatabase
user_db = UserDatabase("user_database.db")

# Initialize other components
byteManager = BytesManager()
partManager = PartitionManager()
partUtils = PartitionFinder(partManager.partition_path)
configHandler = ConfigHandler(os.path.join(os.getcwd(), 'partitions'))

# Configure GitHub OAuth credentials
github = oauth.remote_app(
    'github',
    consumer_key=os.getenv('GITHUB_CLIENT'),
    consumer_secret=os.getenv('GITHUB_SECRET'),
    request_token_params={'scope': 'user:email'},
    base_url='https://api.github.com/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize'
)


def generate_api_key():
    return binascii.hexlify(os.urandom(20)).decode()


@github.tokengetter
def get_github_oauth_token():
    return session.get('github_token')


@app.route('/login')
def login():
    return github.authorize(callback=url_for('authorized', _external=True))


@app.route('/login/authorized')
def authorized():
    resp = github.authorized_response()
    if resp is None or resp.get('access_token') is None:
        return 'Access denied: {0}'.format(
            request.args['error_description']
        )
    session['github_token'] = (resp['access_token'], '')
    user_info = github.get('user')

    # Check if user exists and add if not
    user = user_db.get_user(user_info.data['login'])
    if not user:
        api_key = generate_api_key()
        allocated_space = configHandler.getUserSize()
        allocated_space_str = str(allocated_space) + 'GB'
        allocated_space_bytes = byteManager.ByteDetection(allocated_space_str)

        # Set up cloud partition
        cloud = ConfigHandler.setupDefault(allocated_space_str)
        if cloud:
            try:
                success = user_db.add_user(user_info.data['login'], False, allocated_space_bytes, datetime.now(
                ).strftime("%Y-%m-%d %H:%M:%S"), api_key)
                if not success:
                    logger.error(
                        f"Failed to add user {user_info.data['login']} to database")
                    return jsonify({'message': 'Error adding user to database'}), 500

                partManager.createPartition(
                    key=user_info.data['login'], size_t=allocated_space_bytes)
                logger.info("Partition Created")

                # Add a slight delay to ensure the transaction commits
                time.sleep(1)

                # Retry logic for user retrieval
                for _ in range(3):
                    user = user_db.get_user(user_info.data['login'])
                    if user:
                        logger.info(
                            f"User {user_info.data['login']} retrieved successfully after creation")
                        break
                    time.sleep(1)  # Wait before retrying

                if not user:
                    logger.error(
                        f"Error retrieving user {user_info.data['login']} after creation")
                    return jsonify({'message': 'Error creating user and retrieving from database'}), 500

            except Exception as e:
                logger.exception(
                    "Exception during user creation and partitioning")
                return jsonify({'message': 'Error creating user and partition'}), 500
        else:
            return jsonify({'message': 'Error setting up cloud partition'}), 500

    return 'Logged in as GitHub user {0} with API key {1}'.format(user_info.data['login'], user['api_key'])


@app.route('/api/token')
def get_api_token():
    if 'github_token' in session:
        return jsonify({'access_token': session['github_token'][0]})
    else:
        return 'No GitHub token found.'

# Function to verify API token


def verify_api_token(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        api_token = request.headers.get('API-Token')
        if not api_token:
            return jsonify({'message': 'API token is missing'}), 401

        user = user_db.get_user_by_api_key(api_token)
        if not user:
            return jsonify({'message': 'Invalid API token'}), 401

        return func(user, *args, **kwargs)
    return decorated_function

# API endpoint to get user's premium status


@app.route('/api/premium_status', methods=['GET'])
@verify_api_token
def get_premium_status(user):
    return jsonify({'user_key': user['user_key'], 'premium': user['premium']})

# Helper function to check allowed file types


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {
               'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'exe'}

# File upload endpoint


@app.route('/upload', methods=['POST'])
@verify_api_token
def upload_file(user):
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)

        # Check user's allocated space
        allocated_space = user['allocated_space']
        used_space = user['used_space']
        file_size = len(file.read())
        file.seek(0)  # Reset file pointer after read

        user_partition_path = os.path.join(
            app.config['UPLOAD_FOLDER'], user['user_key'])
        file_path = os.path.join(user_partition_path, filename)
        encrypted_file_path = file_path + '.enc'

        # Check if the file is already registered in the database
        existing_file = user_db.get_user_file(
            user['user_key'], encrypted_file_path)

        if existing_file:
            existing_file_size = existing_file['file_size']
            if file_size > existing_file_size:
                # Increase used space
                used_space += (file_size - existing_file_size)
            elif file_size < existing_file_size:
                # Decrease used space
                used_space -= (existing_file_size - file_size)

            # Update the file's upload date to the current time
            user_db.update_user_file(
                user['user_key'], encrypted_file_path, file_size)
        else:
            used_space += file_size  # Add used space if it's a new file
            user_db.add_user_file(
                user['user_key'], encrypted_file_path, file_size)

        if used_space > allocated_space:
            return jsonify({'message': 'Not enough allocated space'}), 400

        # Ensure the user partition directory exists
        os.makedirs(user_partition_path, exist_ok=True)

        # Save the file to the user's partition
        file.save(file_path)

        # Encrypt the file
        file_encryptor = FileEncryptor(user['api_key'])
        encrypted_file_path = file_encryptor.encrypt_file(file_path)
        os.remove(file_path)  # Remove the original file after encryption

        # Update used space in the partition
        user_db.update_used_space(user['user_key'], used_space)


        return jsonify({'message': 'File successfully uploaded and encrypted', 'allocated_space': allocated_space, 'used_space': used_space}), 201
    else:
        return jsonify({'message': 'File type not allowed'}), 400

# File download endpoint


@app.route('/download/<filename>', methods=['GET'])
@verify_api_token
def download_file(user, filename):
    user_partition_path = os.path.join(
        app.config['UPLOAD_FOLDER'], user['user_key'])
    encrypted_file_path = os.path.join(user_partition_path, filename + '.enc')

    if os.path.exists(encrypted_file_path):
        # Decrypt the file
        file_encryptor = FileEncryptor(user['api_key'])
        decrypted_file_path = file_encryptor.decrypt_file(encrypted_file_path)

        # Create a temporary file for sending
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        shutil.copy(decrypted_file_path, temp_file.name)

        @after_this_request
        def remove_decrypted_file(response):
            try:
                os.remove(decrypted_file_path)
            except Exception as e:
                logger.error(
                    f"Error deleting decrypted file {decrypted_file_path}: {e}")
            return response

        return send_file(temp_file.name, as_attachment=True, download_name=filename)
    else:
        return jsonify({'message': 'File not found'}), 404


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
# curl -X GET -H "API-Token: a01d1e2d1812fcd2f7ecb85bf107d64ec5247193" -o "landingpage.png" http://localhost:5000/download/landingpage.png
# curl -X POST -H "API-Token: a01d1e2d1812fcd2f7ecb85bf107d64ec5247193" -F "file=@Z:\Downloads\landingpage.png" http://localhost:5000/upload
