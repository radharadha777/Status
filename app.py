from flask import Flask, jsonify, send_from_directory
import requests
import threading
import time
import os

app = Flask(__name__)

# ✅ Aapke Nodes (Port 8080 Pterodactyl Wings)
NODES = [
    {"name": "Panel", "url": "https://panel.coramtix.in"},
    {"name": "Node-IN-1", "url": "http://node-in-1.coramtix.in:8080"},
    {"name": "Node-IN-2", "url": "http://node-in-2.coramtix.in:8080"},
    {"name": "Node-IN-3", "url": "http://node-in-3.coramtix.in:8080"},
]

# ✅ Aapka Discord Webhook
DISCORD_WEBHOOK = "YOUR_WEBHOOK_URL_HERE"

status_cache = {}

def send_discord_alert(text):
    try:
        requests.post(DISCORD_WEBHOOK, json={"content": text}, timeout=5)
    except:
        pass

def monitor():
    while True:
        for node in NODES:
            try:
                r = requests.get(node["url"], timeout=4)
                is_up = r.status_code in [200, 403]
            except:
                is_up = False

            prev = status_cache.get(node["name"])
            status_cache[node["name"]] = is_up

            if prev is None:
                continue

            if prev != is_up:
                if is_up:
                    send_discord_alert(f"✅ `{node['name']}` is BACK ONLINE!")
                else:
                    send_discord_alert(f"❌ `{node['name']}` is DOWN!")

        time.sleep(20)

threading.Thread(target=monitor, daemon=True).start()

@app.route("/status")
def status():
    return jsonify(status_cache)

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
