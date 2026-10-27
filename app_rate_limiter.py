import time
import threading
from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory dictionary: user ID -> request timestamps
request_logs = {}
RATE_LIMIT = 5
TIME_WINDOW = 60
logs_lock = threading.Lock()


@app.route("/data", methods=["GET"])
def get_data():
    user_id = (
        request.args.get("user_id")
        or request.headers.get("X-User-ID")
        or request.remote_addr
        or "anonymous"
    )
    current_time = time.time()

    with logs_lock:
        timestamps = request_logs.setdefault(user_id, [])
        # Keep only timestamps from the previous 60 seconds.
        timestamps = [
            timestamp for timestamp in timestamps
            if current_time - timestamp < TIME_WINDOW
        ]
        request_logs[user_id] = timestamps

        if len(timestamps) >= RATE_LIMIT:
            return "Too Many Requests: Try again later.", 429

        timestamps.append(current_time)

        return jsonify({
            "user_id": user_id,
            "message": "Success! Here is your requested data.",
            "requests_in_last_minute": len(timestamps),
            "remaining_quota": RATE_LIMIT - len(timestamps)
        }), 200


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5004, debug=False)
