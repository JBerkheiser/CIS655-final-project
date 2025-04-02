from flask import Flask, jsonify, request
from flask_cors import CORS
from google.cloud import vision

app = Flask(__name__)
CORS(app)

RESPONSE_TABLE = {
    'LABEL_DETECTION': 'label_annotations',
    'FACE_DETECTION': 'face_annotations',
    'LANDMARK_DETECTION': 'landmark_annotations',
    'LOGO_DETECTION': 'logo_annotations',
    'DOCUMENT_TEXT_DETECTION': 'text_annotations',
    'OBJECT_LOCALIZATION': 'localized_object_annotations'
}

@app.route("/get-image-description", methods=["POST"])
def getImageDescription() -> vision.EntityAnnotation:
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file part"}), 400
    
    tasks = request.form.getlist('tasks')
    tasks = tasks[0].split(',')
    if not tasks:
        return jsonify({"error": "No tasks selected"}), 400
    
    print("Selected Tasks: ", tasks)

    features = []
    for task in tasks:
        feature = {"type": getattr(vision.Feature.Type, task)}
        features.append(feature)
    
    image_bytes = file.read()
    image = vision.Image(content=image_bytes)

    client = vision.ImageAnnotatorClient()
    response = client.annotate_image({"image": image, "features": features})
    
    data = {}
    for task in tasks:
        if task in RESPONSE_TABLE:
            result = RESPONSE_TABLE[task]
            if hasattr(response, result):
                data[result] = getattr(response, result)
    
    print("Results: ", data)
    return jsonify({"data": data})

if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)