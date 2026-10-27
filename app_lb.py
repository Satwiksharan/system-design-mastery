import threading
import requests
from flask import Flask, Response

app = Flask(__name__)

BACKEND_PORTS = [5001, 5002, 5003]
HOST_PREFIX = "http://127.0.0.1:"
current_server_index = 0
index_lock = threading.Lock()


def get_next_server():
    """Select the next backend in round-robin order."""
    global current_server_index

    with index_lock:
        port = BACKEND_PORTS[current_server_index]
        current_server_index = (current_server_index + 1) % len(BACKEND_PORTS)

    return f"{HOST_PREFIX}{port}"


@app.route("/", methods=["GET"])
def router():
    target_server = get_next_server()

    try:
        backend_response = requests.get(target_server, timeout=3)
        return Response(
            backend_response.content,
            status=backend_response.status_code,
            content_type=backend_response.headers.get("Content-Type", "text/plain")
        )
    except requests.exceptions.RequestException as error:
        return f"Backend Server ({target_server}) is unreachable: {error}\n", 502


if __name__ == "__main__":
    print("Load Balancer running on port 8080...")
    app.run(host="127.0.0.1", port=8080, debug=False)
