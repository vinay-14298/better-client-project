from flask import Flask, request, jsonify
import mysql.connector
import boto3
import json

app = Flask(__name__)

# Fetch secrets from AWS Secrets Manager
def get_secrets():
    client = boto3.client('secretsmanager', region_name='us-east-2')  # Replace with your AWS region
    secret_name = "mysql/container"  # Replace with your secret name

    response = client.get_secret_value(SecretId=secret_name)
    secrets = json.loads(response['SecretString'])
    return secrets

# Initialize secrets
secrets = get_secrets()
db_host = secrets['DB_HOST']
db_user = secrets['DB_USER']
db_password = secrets['DB_PASSWORD']
db_name = secrets['DB_NAME']

# MySQL connection function
def get_db_connection():
    conn = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )
    return conn

# Home route (Hello, World!)
@app.route('/')
def home():
    return 'Hello, World!'

# Login route
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user:
        return jsonify({'message': 'Login successful!'}), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401

# Signup route (example)
@app.route('/signup', methods=['POST'])
def signup():
    username = request.json.get('username')
    password = request.json.get('password')
    # Add signup logic to insert the user into the database
    return jsonify({'message': 'Signup successful!'}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

