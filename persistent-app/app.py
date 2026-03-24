from flask import Flask, request, jsonify
import os

app = Flask(__name__)
DATA_DIR = "/data"
os.makedirs(DATA_DIR, exist_ok=True)

@app.route("/word", methods=["POST"])
def save_word():
    data = request.get_json()
    if not data or "word" not in data:
        return {"error": "Send JSON with 'word'"}, 400

    filename = os.path.join(DATA_DIR, "words.txt")
    with open(filename, "a", encoding="utf-8") as f:
        f.write(data["word"] + "\n")

    return {"status": "saved", "word": data["word"]}, 200

@app.route("/words", methods=["GET"])
def list_words():
    filename = os.path.join(DATA_DIR, "words.txt")
    if not os.path.exists(filename):
        return {"words": []}, 200

    with open(filename, "r", encoding="utf-8") as f:
        words = [line.strip() for line in f.readlines()]

    return {"words": words}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
