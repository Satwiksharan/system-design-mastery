import sys
from flask import Flask

app = Flask(__name__)

# Usage: python app_backend.py <server_id> <port>
SERVER_ID = sys.argv[1] if len(sys.argv) > 1 else "1"
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 5001


@app.route("/", methods=["GET"])
def home():
    return f"Hello from Server {SERVER_ID}!\n", 200


if __name__ == "__main__":
    print(f"Starting Mock Server {SERVER_ID} on port {PORT}...")
    app.run(host="127.0.0.1", port=PORT, debug=False)
