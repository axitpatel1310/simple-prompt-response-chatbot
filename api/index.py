# api/index.py
from flask import Flask, request, jsonify, render_template
import json
import os

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), "..", "templates"))

def load_dataset(path=None):
    if path is None:
        path = os.path.join(os.path.dirname(__file__), "..", "dataset.jsonl")
    path = os.path.abspath(path)
    dataset = []
    if not os.path.exists(path):
        print(f"dataset not found at {path}")
        return dataset

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                dataset.append(json.loads(line))
            except Exception as e:
                print(f"skipping bad line: {e}")
    return dataset

def get_response(user_input, dataset):
    user_input = user_input.lower().strip()
    for item in dataset:
        prompts = item.get("prompts", [])
        for prompt in prompts:
            if user_input == prompt.lower():
                return item.get("response", "")
    return "Sorry, but what was that? I didnt get it.."

DATASET = load_dataset()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json() or {}
    msg = data.get("message", "")
    if not msg:
        return jsonify({"error": "no message"}), 400
    resp = get_response(msg, DATASET)
    return jsonify({"response": resp})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
