import os
import json
import requests
from flask import Flask, jsonify
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Hello from Cloud Foundry!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 8080)))
