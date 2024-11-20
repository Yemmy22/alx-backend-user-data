#!/usr/bin/env python3
"""
A flask app module
"""
from flask import Flask, jsonify

# Create a Flask application instance
app = Flask(__name__)


# Define a route for the root URL
@app.route('/')
def hello_world():
    return jsonify(message="Bienvenue")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
