from flask import Flask, jsonify
from flask_cors import CORS
import db

app = Flask(__name__)
CORS(app)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/transactions")
def get_transactions(limit=10):
    limit = 10 if limit is None else limit
    result = db.get_transactions_num(limit)
    json = jsonify(result)
    return json


@app.route("/window/<id>/<time>")
def get_hit(id, time):
    if id is None or time is None:
        return None
    result = db.transaction_window(id, time)
    json = jsonify(result)
    return json
