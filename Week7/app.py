from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

API_KEY = "YOUR_API_KEY"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/stock/<symbol>")
def stock(symbol):

    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={API_KEY}"

    r = requests.get(url)
    data = r.json()

    if "Global Quote" not in data or data["Global Quote"] == {}:
        return jsonify({"error": "Invalid symbol"})

    stock = data["Global Quote"]

    return jsonify({
        "symbol": stock["01. symbol"],
        "price": stock["05. price"],
        "change": stock["09. change"],
        "percent": stock["10. change percent"]
    })


@app.route("/history/<symbol>")
def history(symbol):

    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}"

    r = requests.get(url)
    data = r.json()

    series = data["Time Series (Daily)"]

    dates = []
    prices = []

    for date in sorted(series.keys())[-365:]:
        dates.append(date)
        prices.append(float(series[date]["4. close"]))

    latest = prices[-1]
    old = prices[0]

    change = latest - old
    percent = (change / old) * 100

    return jsonify({
        "dates": dates,
        "prices": prices,
        "year_change": round(change,2),
        "year_percent": round(percent,2)
    })


if __name__ == "__main__":
    app.run(debug=True)