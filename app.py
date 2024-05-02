from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

# MongoDB configuration
uri = 'mongodb+srv://asdevlopers02:6fXfDFKNImSUAiKJ@cluster0.us8nw6q.mongodb.net/'

client = MongoClient(uri)
db = client['user_database']
users_collection = db['users']

# Signup API
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data['username']
    email = data['email']
    password = data['password']

    if users_collection.find_one({'email': email}):
        return jsonify({'message': 'Username already exists'}), 400

    # Insert user into the database
    user = {'username': username, 'email':email, 'password': password}
    users_collection.insert_one(user)

    return jsonify({'message': 'User created successfully'}), 201

# Login API
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data['email']
    password = data['password']

    # Check if the user exists
    user = users_collection.find_one({'email': email})

    if not user or user['password'] != password:
        return jsonify({'message': 'Invalid username or password'}), 401
    
    return jsonify({'message': 'Login successful'}), 200

if __name__ == '__main__':
    app.run(debug=True)
