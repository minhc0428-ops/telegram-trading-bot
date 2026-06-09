from flask import Flask, request
import requests

app = Flask(__name__)

TOKEN = "8547129446:AAF6Nd42RZlgx6W_GM-DEHKxJag0YmOorU4"
CHAT_ID = "-1002561812973"


def send(text):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": text})
    except Exception as e:
        print("Telegram error:", e)


@app.route("/")
def home():
    return "BOT RUNNING"


@app.route("/run")
def run():
    send("🟢 BOT TEST OK - Render Working")
    return "OK"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
