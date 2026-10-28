import os
import sqlite3
import subprocess

from flask import Flask, jsonify, request

app = Flask(__name__)

# VULNERABILITY 1: Hardcoded secret
API_SECRET = "lab_test_secret_123456789"

DATABASE = "users.db"


def init_db():
    """Create a small database for the lab."""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL
        )
    """)

    cursor.execute(
        "INSERT OR IGNORE INTO users (id, username) VALUES (1, 'alex')"
    )

    conn.commit()
    conn.close()


@app.route("/")
def home():
    return jsonify(message="Welcome to the vulnerable DevSecOps lab")


@app.route("/health")
def health():
    return jsonify(status="ok"), 200


# VULNERABILITY 2: SQL Injection
@app.route("/api/search")
def search_user():
    username = request.args.get("username", "")

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Intentionally unsafe: user input is concatenated into SQL.
    query = f"SELECT id, username FROM users WHERE username = '{username}'"

    try:
        cursor.execute(query)
        results = cursor.fetchall()
        return jsonify([
            {"id": row[0], "username": row[1]}
            for row in results
        ])
    finally:
        conn.close()


# VULNERABILITY 3: OS Command Injection
@app.route("/api/ping")
def ping():
    host = request.args.get("host", "127.0.0.1")

    # Intentionally unsafe: shell=True with user-controlled input.
    result = subprocess.run(
        f"ping -c 1 {host}",
        shell=True,
        capture_output=True,
        text=True,
        timeout=5
    )

    return jsonify(output=result.stdout)


# VULNERABILITY 4: Debug mode enabled
if __name__ == "__main__":
    init_db()
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
