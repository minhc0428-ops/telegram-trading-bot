from flask import Flask, request
import requests

app = Flask(__name__)

TOKEN = "8547129446:AAF6Nd42RZlgx6W_GM-DEHKxJag0YmOorU4"
CHAT_ID = "-1002561812973"

# ======================
# TELEGRAM SEND
# ======================
def send(msg):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": msg})
    except Exception as e:
        print("Telegram error:", e)

# ======================
# GET BINANCE PRICE
# ======================
def get_price(symbol="BTCUSDT"):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    data = requests.get(url).json()
    return float(data["price"])

# ======================
# SIMPLE SUPER TREND LOGIC (STABLE VERSION)
# ======================
def get_trend(prices, period=10):
    if len(prices) < period:
        return None

    ma = sum(prices[-period:]) / period
    return ma

# ======================
# BOT LOOP
# ======================
def bot_loop():
    prices = []
    prev_trend = None

    while True:
        try:
            price = get_price("BTCUSDT")
            prices.append(price)

            # giữ dữ liệu nhẹ
            if len(prices) > 50:
                prices.pop(0)

            ma = get_trend(prices, 10)

            if ma is None:
                time.sleep(10)
                continue

            trend = price > ma  # TRUE = BUY bias

            if prev_trend is not None and trend != prev_trend:
                if trend:
                    send(f"🟢 BUY SIGNAL BTC\nPrice: {price}\nMA10: {ma}")
                else:
                    send(f"🔴 SELL SIGNAL BTC\nPrice: {price}\nMA10: {ma}")

            prev_trend = trend

            time.sleep(30)

        except Exception as e:
            print("Loop error:", e)
            time.sleep(10)

# ======================
# ROUTES
# ======================
@app.route("/")
def home():
    return "BOT RUNNING"

@app.route("/run")
def run():
    send("🟢 MANUAL TEST OK - BOT WORKING")
    return "OK"

# ======================
# START BACKGROUND BOT
# ======================
threading.Thread(target=bot_loop, daemon=True).start()

# ======================
# START SERVER
# ======================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
