import os
<<<<<<< HEAD
import sqlite3
import subprocess

from flask import Flask, jsonify, request
=======

from flask import Flask, jsonify
>>>>>>> a1cf47b (update app to be not vulnerable)


<<<<<<< HEAD
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
=======
def create_app():
    app = Flask(__name__)

    # Application configuration
    app.config.update(
        DEBUG=False,
        TESTING=False,
        MAX_CONTENT_LENGTH=16 * 1024,
        TRUSTED_HOSTS=os.getenv(
            "TRUSTED_HOSTS",
            "localhost,127.0.0.1"
        ).split(","),
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
    )

    # Security headers
    @app.after_request
    def security_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Content-Security-Policy"] = (
            "default-src 'none'; "
            "frame-ancestors 'none'; "
            "base-uri 'none'"
        )
        response.headers["Permissions-Policy"] = (
            "camera=(), microphone=(), geolocation=()"
        )

        return response

    # Homepage
    @app.route("/", methods=["GET"])
    def home():
        return jsonify({
            "application": "Secure Flask Demo",
            "status": "running",
            "message": "Welcome to the secure application."
        })

    # Health endpoint
    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({
            "status": "healthy"
        }), 200

    # Generic error handling
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "error": "Resource not found"
        }), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            "error": "Internal server error"
        }), 500

    return app


app = create_app()
>>>>>>> a1cf47b (update app to be not vulnerable)
