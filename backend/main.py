from flask import Flask, jsonify, request
from flask_cors import CORS
from google.cloud import vision

app = Flask(__name__)
CORS(app)

@app.route("/get-image-description", methods=["POST"])
def getImageDescription() -> vision.EntityAnnotation:
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file part"}), 400
    
    image_bytes = file.read()
    image = vision.Image(content=image_bytes)

    client = vision.ImageAnnotatorClient()
    response = client.label_detection(image=image)
    labels = response.label_annotations

    label_data = [{"description": label.description, "score": label.score} for label in labels]

    return jsonify({"labels": label_data}) 

if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)