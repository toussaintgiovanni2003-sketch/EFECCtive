from flask import Flask, request, jsonify, render_template
import json, threading, os

app = Flask(__name__)

DATA_FILE = "codes.json"
lock = threading.Lock()

def load_codes():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_codes(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/verify", methods=["POST"])
def verify():
    data = request.get_json()
    code = data.get("code", "").strip().upper()

    if not code:
        return jsonify({"status": "invalid", "message": "Enter a code"})

    with lock:
        codes = load_codes()

        if code not in codes:
            return jsonify({"status": "invalid", "message": "Invalid cheque number"})

        if codes[code]:
            return jsonify({"status": "used", "message": "Cheque already used"})

        codes[code] = True
        save_codes(codes)

    return jsonify({"status": "valid", "message": "Valid cheque"})

if __name__ == "__main__":
    app.run(debug=True)
