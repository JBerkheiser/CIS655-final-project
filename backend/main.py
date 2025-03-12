from flask import Flask, jsonify
import requests
from flask_cors import CORS
from google.cloud import vision

app = Flask(__name__)
CORS(app)

@app.route("/get-image-description")
def getImageDescription() -> vision.EntityAnnotation:
    client = vision.ImageAnnotatorClient()
    file_uri = "https://miamivalleytoday.com/wp-content/uploads/2023/10/132048163_web1_ideal-neighborhood.jpg"

    image = vision.Image()
    image.source.image_uri = file_uri

    # Performs label detection on the image file
    response = client.label_detection(image=image)
    labels = response.label_annotations

    print("Labels:")
    for label in labels:
        print(label.description)

    return labels

if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)