from flask import Flask, request
import requests

app = Flask(__name__)

TOKEN = "8547129446:AAF6Nd42RZlgx6W_GM-DEHKxJag0YmOorU4"
CHAT_ID = "-1002561812973"

def send(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})


# --- SUPER TREND ---
def supertrend(df, period=10, multiplier=3):
    hl2 = (df['high'] + df['low']) / 2
    atr = df['high'] - df['low']
    atr = atr.rolling(period).mean()

    upper = hl2 + multiplier * atr
    lower = hl2 - multiplier * atr

    trend = [True]

    for i in range(1, len(df)):
        if df['close'][i] > upper[i-1]:
            trend.append(True)
        elif df['close'][i] < lower[i-1]:
            trend.append(False)
        else:
            trend.append(trend[i-1])

    return trend


@app.route("/")
def home():
    return "BOT RUNNING"


@app.route("/run")
def run_bot():

    # giả lập dữ liệu (sau sẽ nâng cấp real data Binance)
    import yfinance as yf

    df = yf.download("BTC-USD", period="1d", interval="5m")

    df = df.dropna()

    trend = supertrend(df)

    if trend[-1] == True:
        send("🟢 BUY SIGNAL BTC")
    else:
        send("🔴 SELL SIGNAL BTC")

    return "ok"


app.run(host="0.0.0.0", port=10000)
