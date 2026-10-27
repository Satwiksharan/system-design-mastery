from flask import Flask, request, jsonify, redirect
import threading

app = Flask(__name__)

# In-memory mapping: short ID -> original URL
url_db = {}
counter = 100000
counter_lock = threading.Lock()
BASE62_ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def encode_base62(num):
    """Convert a base-10 integer into a Base62 string."""
    if num == 0:
        return BASE62_ALPHABET[0]

    encoded = []
    base = len(BASE62_ALPHABET)

    while num > 0:
        num, remainder = divmod(num, base)
        encoded.append(BASE62_ALPHABET[remainder])

    return "".join(reversed(encoded))


@app.route("/shorten", methods=["POST"])
def shorten_url():
    global counter

    data = request.get_json(silent=True) or {}
    long_url = data.get("url")

    if not isinstance(long_url, str) or not long_url.strip():
        return jsonify(error="Please provide a valid 'url' in the JSON body."), 400

    long_url = long_url.strip()
    if not long_url.startswith(("http://", "https://")):
        return jsonify(error="URL must start with http:// or https://."), 400

    with counter_lock:
        counter += 1
        short_id = encode_base62(counter)
        url_db[short_id] = long_url

    return jsonify({
        "original_url": long_url,
        "short_id": short_id,
        "short_url": request.host_url.rstrip("/") + "/" + short_id
    }), 201


@app.route("/<short_id>", methods=["GET"])
def redirect_to_url(short_id):
    long_url = url_db.get(short_id)

    if long_url:
        return redirect(long_url, code=302)

    return jsonify(error="Short URL ID not found."), 404


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
