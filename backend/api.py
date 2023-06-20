from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_cors.decorator import cross_origin
import pandas as pd

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route("/api/search", methods=['GET'])
@cross_origin()
def getMotors():
    r = request
    r = r.args
    name = r.get("name")
    maxPrice = int(r.get("maxPrice"))
    minPrice = int(r.get("minPrice"))
    if name == None:
        name = ""
    if maxPrice == None:
        maxPrice = 100000000000000
    if minPrice == None:
        minPrice = 0
    data = pd.read_csv('../final_data.csv')
    result = data[(data['price'] >= minPrice) & (data['price'] <= maxPrice) & (data['name'].str.contains(name, case=False))]
    return jsonify(result.to_dict(orient='records')), 200

@app.route("/api/list", methods=['GET'])
@cross_origin()
def getAll():
    r = request
    r = r.args
    page = int(r.get("page"))
    data = pd.read_csv('../final_data.csv')
    idx = (page - 1) * 18
    data = data[idx: idx + 18]
    data = data.to_dict(orient='records')
    return jsonify(data), 200

@app.route("/api/total", methods=['GET'])
@cross_origin()
def getTotal():
    data = pd.read_csv('../final_data.csv')
    l = len(data)
    return jsonify(l), 200

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)