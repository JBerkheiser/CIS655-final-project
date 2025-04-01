from flask import Flask, jsonify, request
from flask_cors import CORS
from google.cloud import vision

app = Flask(__name__)
CORS(app)

@app.route("/get-image-description", methods=["POST"])
def getLogoDescription() -> vision.EntityAnnotation:
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file part"}), 400
    
    tasks = request.form.getlist('tasks')
    if not tasks:
        return jsonify({"error": "No tasks selected"}), 400
    
    print(tasks)
    
    image_bytes = file.read()
    image = vision.Image(content=image_bytes)

    client = vision.ImageAnnotatorClient()
    response = client.logo_detection(image=image)
    logos = response.logo_annotations

    logo_data = [{"description": logo.description, "score": logo.score} for logo in logos]

    return jsonify({"logos": logo_data}) 

if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)