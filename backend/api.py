from flask import Flask, request, jsonify
from flask.wrappers import Response
from flask_cors import CORS
from flask_cors.decorator import cross_origin
from controller import BL
import json
import pandas as pd

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route("/api/search", methods=['GET'])
@cross_origin()
def getMotors():
    r = request
    r = r.args
    name = r.get("name")
    maxPrice = r.get("maxPrice")
    minPrice = r.get("minPrice")
    if name == None:
        name = ""
    if maxPrice == None:
        maxPrice = ""
    if minPrice == None:
        minPrice = ""
    bl = BL()
    result = bl.filter(name, maxPrice, maxPrice)
    result = {
        "test": "test api"
    }
    result = json.dumps(result, ensure_ascii=False)
    return Response(response=result, status=200, mimetype="application/json")

@app.route("/api/list", methods=['GET'])
@cross_origin()
def getAll():
    r = request
    r = r.args
    page = int(r.get("page"))
    data = pd.read_csv('../crawl/crawl/spiders/all_data/muaban.csv')
    print(page)
    idx = (page - 1) * 18
    print(idx)
    data = data[idx: idx + 18]
    return jsonify(data.to_dict(orient='records'))

@app.route("/api/total", methods=['GET'])
@cross_origin()
def getTotal():
    data = pd.read_csv('../crawl/crawl/spiders/all_data/muaban.csv')
    l = len(data)
    return jsonify(l)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)