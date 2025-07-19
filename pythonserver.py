from flask import Flask, request, jsonify
from prophet import Prophet
import pandas as pd
from datetime import timedelta

app = Flask(__name__)
print("Server Spinning up")
# prophet


@app.route("/", methods=["GET"])
def a2():
    print("Request method:", request.method)
    return jsonify({"res": 50})


@app.route("/analysis", methods=["POST"])
def a1():
    print("Prophet Modelling Request Received")
    json = request.json
    # print("request data", json)
    CPUdata = json["data"][0]["CPUUtilization"]
    # print("cpudata", CPUdata)
    if not CPUdata:
        return jsonify({"error": "Missing or invalid data"}), 400
    df = pd.DataFrame(
        {
            "ds": pd.to_datetime(
                pd.Series(CPUdata["Timestamps"]), utc=True
            ).dt.tz_convert(None),
            "y": CPUdata["Values"],
        }
    )
    model = Prophet(interval_width=0.95)
    model.fit(df)

    future = model.make_future_dataframe(periods=60, freq="10min")

    forecast = model.predict(future)
    tail = forecast.tail(20)

    # See forecast
    res = tail[["ds", "yhat"]]
    res.to_dict(orient="records")

    return jsonify(res.to_dict(orient="records"))


if __name__ == "__main__":
    app.run(debug=False, port=5050, host="127.0.0.1")
