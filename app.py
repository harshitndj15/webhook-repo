from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow CORS for frontend polling

client = MongoClient("mongodb://localhost:27017/")  # Replace with your Mongo URI
db = client.github_events
collection = db.events

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    event_type = request.headers.get('X-GitHub-Event')
    
    payload = {}

    if event_type == "push":
        payload = {
            "author": data["pusher"]["name"],
            "to_branch": data["ref"].split("/")[-1],
            "timestamp": datetime.utcnow().isoformat(),
            "event": "push"
        }
    elif event_type == "pull_request":
        payload = {
            "author": data["pull_request"]["user"]["login"],
            "from_branch": data["pull_request"]["head"]["ref"],
            "to_branch": data["pull_request"]["base"]["ref"],
            "timestamp": datetime.utcnow().isoformat(),
            "event": "pull_request"
        }

    if payload:
        collection.insert_one(payload)
        return jsonify({"status": "saved"}), 201

    return jsonify({"status": "ignored"}), 200

@app.route('/events', methods=['GET'])
def get_events():
    events = list(collection.find({}, {"_id": 0}))
    return jsonify(events)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
