# pyright: reportMissingImports=false
from flask import Flask, jsonify  
import os
import socket
import pymysql

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

@app.route("/db-check")
def db_check():
    try:
        connection = pymysql.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME", "appdb"),
            port=int(os.getenv("DB_PORT", 3306)),
            connect_timeout=3
        )
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
        connection.close()
        
        return jsonify(
            status="success",
            message="Successfully connected to RDS MySQL database!",
            db_test_query=result[0]
        ), 200
    except Exception as e:
        return jsonify(
            status="error",
            message="Failed to connect to database",
            error_details=str(e)
        ), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)