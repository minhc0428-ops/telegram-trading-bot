from flask import Flask, request
import requests

app = Flask(__name__)

TOKEN = "8547129446:AAF6Nd42RZlgx6W_GM-DEHKxJag0YmOorU4"
CHAT_ID = "-1002561812973"

def send(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    message = f"""
🚨 SIGNAL

Pair: {data.get('symbol')}
Side: {data.get('side')}
Entry: {data.get('entry')}
SL: {data.get('sl')}
TP: {data.get('tp')}
"""

    send(message)
    return "ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
