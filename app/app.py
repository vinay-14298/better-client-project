from flask import Flask, render_template, request, jsonify, redirect, url_for
import mysql.connector
import boto3
import json

app = Flask(__name__)

# Fetch secrets from AWS Secrets Manager
def get_secrets():
    try:
        client = boto3.client('secretsmanager', region_name='us-east-2')  # Replace with your AWS region
        secret_name = "mysql/container"  # Replace with your secret name

        response = client.get_secret_value(SecretId=secret_name)
        secrets = json.loads(response['SecretString'])
        return secrets
    except Exception as e:
        print(f"Error fetching secrets: {e}")
        return None

# Initialize secrets
secrets = get_secrets()
if secrets:
    db_host = secrets['DB_HOST']
    db_user = secrets['DB_USER']
    db_password = secrets['DB_PASSWORD']
    db_name = secrets['DB_NAME']
else:
    print("Failed to fetch secrets, exiting.")
    exit(1)

# MySQL connection function
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name,
            auth_plugin='caching_sha2_password'
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        conn = get_db_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
            user = cursor.fetchone()
            cursor.close()
            conn.close()

            if user:
                return redirect(url_for('login_success'))
            else:
                return jsonify({'message': 'Invalid username or password'}), 401
        else:
            return jsonify({'message': 'Database connection failed'}), 500

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor(dictionary=True)
                cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, password))
                conn.commit()
                cursor.close()
                conn.close()

                return redirect(url_for('register_success'))
            except mysql.connector.Error as err:
                print(f"Error during registration: {err}")
                return jsonify({'message': 'Error during registration'}), 500
        else:
            return jsonify({'message': 'Database connection failed'}), 500

    return render_template('register.html')

@app.route('/login_success')
def login_success():
    return render_template('login_success.html')

@app.route('/register_success')
def register_success():
    return render_template('register_success.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

