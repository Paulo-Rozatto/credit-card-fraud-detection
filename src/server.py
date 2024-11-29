from flask import Flask, jsonify, Response
from flask_cors import CORS
import db
import matplotlib.pyplot as plt
import io
import datetime
import base64

from utils import rules_prediction

app = Flask(__name__)
CORS(app)


@app.route("/transactions")
def get_transactions(limit=10):
    limit = 10 if limit is None else limit
    result = db.get_transactions_num(limit)
    json = jsonify(result)
    return json


@app.route("/window/<id>/<time>")
def get_window(id, time):
    if id is None or time is None:
        return None
    result = db.transaction_window(id, time)

    entry = []
    for block in result:
        entry += list(block)
    entry.reverse()
    entry = entry[:-1]

    prediction_array = rules_prediction(entry)

    amounts = [entry[0] for entry in result]
    times = [datetime.datetime.fromtimestamp(entry[3]) for entry in result]
    is_fraud = [entry[4] for entry in result]

    amounts.reverse()
    times.reverse()
    is_fraud.reverse()

    # Create the plot
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(times, amounts, label='Amount over Time', color='blue', marker='o')

    # Highlight fraudulent points
    fraud_times = [times[i] for i in range(len(is_fraud)) if is_fraud[i]]
    fraud_amounts = [amounts[i] for i in range(len(is_fraud)) if is_fraud[i]]
    ax.scatter(fraud_times, fraud_amounts,
               color='red', label='Fraud', zorder=5)

    ax.set_xlabel('Time')
    ax.set_ylabel('Amount')
    ax.set_title('Amount over Time with Fraud Highlights')
    ax.tick_params(axis='x', labelrotation=45)
    ax.legend()

    # Save the plot to a BytesIO object as SVG
    output = io.BytesIO()
    plt.tight_layout()
    plt.savefig(output, format='svg')
    plt.close(fig)
    output.seek(0)

    svg_base64 = base64.b64encode(output.getvalue()).decode('utf-8')

    return jsonify({
        "prediction_array": prediction_array,
        "svg": f"data:image/svg+xml;base64,{svg_base64}"
    })

    # return Response(output.getvalue(), content_type='image/svg+xml')
