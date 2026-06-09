from flask import Flask, request
import requests

app = Flask(__name__)

TOKEN = "8547129446:AAF6Nd42RZlgx6W_GM-DEHKxJag0YmOorU4"
CHAT_ID = "-1002561812973"

from flask import Flask
import requests
import time
import threading

app = Flask(__name__)

TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "-1002561812973"

# =====================
# SEND TELEGRAM
# =====================
def send(msg):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": msg})
    except Exception as e:
        print("Telegram error:", e)


# =====================
# GET PRICE BINANCE
# =====================
def get_price(symbol="BTCUSDT"):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    data = requests.get(url).json()
    return float(data["price"])


# =====================
# SIMPLE SUPER TREND (LIGHT VERSION)
# =====================
def fake_supertrend(price, prev):
    # logic đơn giản hóa để chạy ổn định server
    if prev is None:
        return True

    if price > prev:
        return True
    else:
        return False


# =====================
# BOT LOOP
# =====================
def bot_loop():
    prev_price = None
    prev_trend = None

    while True:
        price = get_price("BTCUSDT")

        trend = fake_supertrend(price, prev_price)

        if prev_trend is not None:
            if trend != prev_trend:
                if trend:
                    send(f"🟢 BUY SIGNAL BTC\nPrice: {price}")
                else:
                    send(f"🔴 SELL SIGNAL BTC\nPrice: {price}")

        prev_price = price
        prev_trend = trend

        time.sleep(60)  # mỗi 1 phút


# =====================
# ROUTES
# =====================
@app.route("/")
def home():
    return "BOT RUNNING"

@app.route("/run")
def run():
    send("🟢 BOT MANUAL TEST OK")
    return "OK"


# =====================
# START BACKGROUND THREAD
# =====================
threading.Thread(target=bot_loop).start()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
