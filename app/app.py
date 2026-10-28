from flask import Flask, jsonify

app = Flask(__name__)

_USERS = {
    1: {"id": 1, "name": "Alex"},
    2: {"id": 2, "name": "Sam"},
}


@app.get("/")
def home():
    return jsonify(message="Welcome to the DevSecOps handover app")


@app.get("/health")
def health():
    return jsonify(status="ok"), 200


@app.get("/api/users/<int:user_id>")
def get_user(user_id: int):
    user = _USERS.get(user_id)
    if user is None:
        return jsonify(error="User not found"), 404
    return jsonify(user), 200


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
