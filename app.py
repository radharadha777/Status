from fastapi import FastAPI
import requests
import threading
import time
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

WEBHOOK = "https://discord.com/api/webhooks/1429028428639637548/ATe0k-CuzwTGRXMAioG0kA-V4nj3_m4PJzT7cFUtnPoYONVwBitWO2jR3tWvln6xGmir"

nodes = {
    "Panel": {"url": "https://panel.coramtix.in", "status": None},
    "Node-1": {"url": "http://node1.cormtix.in:8080", "status": None},
    "Node-2": {"url": "http://node2.cormtix.in:8080", "status": None},
    "Node-3": {"url": "http://node3.cormtix.in:8080", "status": None},
}

def send_webhook(name, state):
    data = {
        "content": f"🚨 **{name} is now {state}**"
    }
    requests.post(WEBHOOK, json=data)

def check_nodes():
    while True:
        for name, node in nodes.items():
            try:
                r = requests.get(node["url"], timeout=5)
                new_status = "Online" if r.status_code == 200 else "Offline"
            except:
                new_status = "Offline"

            if node["status"] is None:
                node["status"] = new_status
            elif node["status"] != new_status:
                node["status"] = new_status
                send_webhook(name, new_status)

        time.sleep(30)

threading.Thread(target=check_nodes, daemon=True).start()

@app.get("/status")
def get_status():
    return nodes
