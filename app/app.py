# pyright: reportMissingImports=false
from flask import Flask, jsonify  
import os
import socket

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify(
        status="healthy",
        message="Hello from AWS DevOps 3-tier project!",
        hostname=socket.gethostname(),
        environment=os.getenv("ENVIRONMENT", "production")
    )

@app.route("/health")
def health_check():
    return jsonify(status="UP"), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)