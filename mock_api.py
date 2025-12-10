# mock_api.py -- Safe mock API for testing
from flask import Flask, request, jsonify
import sarfraz_safe as backend

app = Flask(__name__)

@app.route("/parse_cards", methods=["POST"])
def parse_cards():
    data = request.get_json() or {}
    return jsonify(backend.parse_cards_from_text(data.get("input_text", "")))

@app.route("/start_checking", methods=["POST"])
def start_checking():
    data = request.get_json() or {}
    cards = data.get("cards", [])
    return jsonify(backend.start_checking(cards, gateway=data.get("gateway", "safe")))

@app.route("/get_progress/<session_id>", methods=["GET"])
def get_progress(session_id):
    return jsonify(backend.get_progress(session_id))

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
