from flask import Flask, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/get-image-description")
def getImageDescription():
    projectID = "cis655-vision-api-project"
    jsonContent = ""
    contentType = "application/json; charset=utf-8"
    visionAPIURL = "https://vision.googleapis.com/v1/images:annotate"
    requestHeaders = {"x-goog-user-project": projectID, "Content-Type": contentType}

    with open("request.json", "r") as file:
        jsonContent = file.read()

    generatedDescription = requests.post(visionAPIURL, json=jsonContent, headers=requestHeaders)
    # curl -X POST \
    # -H "Authorization: Bearer $(gcloud auth print-access-token)" \
    # -H "x-goog-user-project: PROJECT_ID" \
    # -H "Content-Type: application/json; charset=utf-8" \
    # https://vision.googleapis.com/v1/images:annotate -d @request.json
    return generatedDescription

if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)