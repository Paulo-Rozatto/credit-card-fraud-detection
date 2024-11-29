from flask import Flask, jsonify
from flask_cors import CORS
import db
import matplotlib.pyplot as plt
import io
import datetime
import base64

from utils import rules_prediction, ann_prediction

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
    prediction_ann = ann_prediction(entry)
    print(prediction_ann)

    amounts = [entry[0] for entry in result]
    times = [datetime.datetime.fromtimestamp(entry[3]) for entry in result]
    is_fraud = [entry[4] for entry in result]

    amounts.reverse()
    times.reverse()
    is_fraud.reverse()

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(times, amounts, label='Quantidades ao Longo do Tempo',
            color='blue', marker='o')

    fraud_times = [times[i] for i in range(len(is_fraud)) if is_fraud[i]]
    fraud_amounts = [amounts[i] for i in range(len(is_fraud)) if is_fraud[i]]
    ax.scatter(fraud_times, fraud_amounts,
               color='red', label='Fraude', zorder=5)

    ax.set_xlabel('Tempo')
    ax.set_ylabel('Quantidade')
    ax.set_title('Quantidade de Compras Recentes')
    ax.tick_params(axis='x', labelrotation=45)
    ax.legend()

    output = io.BytesIO()
    plt.tight_layout()
    plt.savefig(output, format='svg')
    plt.close(fig)
    output.seek(0)

    svg_base64 = base64.b64encode(output.getvalue()).decode('utf-8')

    return jsonify({
        "prediction_array": prediction_array,
        "prediction_ann": prediction_ann,
        "svg": f"data:image/svg+xml;base64,{svg_base64}"
    })
