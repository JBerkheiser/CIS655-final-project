from flask import Flask, jsonify
import random
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/get-problem")
def getMathProblem():
    operatorList = ['+', '-', '*', '/']
    firstNumber = 3
    secondNumber = 45
    operator = random.choice(operatorList)

    retString = jsonify({"firstNumber": firstNumber, "secondNumber": secondNumber, "operator": operator})
    return retString

if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)