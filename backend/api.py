from flask import Flask, request, jsonify
from flask.wrappers import Response
from flask_cors import CORS
from flask_cors.decorator import cross_origin
from controller import BL
import json

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route("/api/motors", methods=['GET'])
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

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)