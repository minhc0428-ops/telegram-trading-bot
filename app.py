from flask import Flask, request
import requests

app = Flask(__name__)

TOKEN = "8547129446:AAF6Nd42RZlgx6W_GM-DEHKxJag0YmOorU4"
CHAT_ID = "-1002561812973"

# ======================
# FUNCTION SEND TELEGRAM
# ======================
def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text
    }
    requests.post(url, data=payload)


# ======================
# HOME CHECK
# ======================
@app.route("/")
def home():
    return "BOT RUNNING"


# ======================
# TEST ROUTE (QUAN TRỌNG)
# ======================
@app.route("/run")
def run():
    send_message("🟢 BOT TEST OK - Telegram Connected")
    return "OK - message sent"


# ======================
# START SERVER
# ======================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
