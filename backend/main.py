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

def getData(task, annotations):
    result = []
    for annotation in annotations:
        task_data = {}
        
        if task == "LABEL_DETECTION" or task == "LOGO_DETECTION":
            task_data["description"] = annotation.description
            task_data["score"] = annotation.score
        elif task == "FACE_DETECTION":
            task_data["rollAngle"] = annotation.rollAngle
            task_data["panAngle"] = annotation.panAngle
            task_data["tiltAngle"] = annotation.tiltAngle
            task_data["detectionConfidence"] = annotation.detectionConfidence
            task_data["landmarkingConfidence"] = annotation.landmarkingConfidence
            task_data["joyLikelihood"] = annotation.joyLikelihood
            task_data["sorrowLikelihood"] = annotation.sorrowLikelihood
            task_data["angerLikelihood"] = annotation.angerLikelihood
            task_data["surpriseLikelihood"] = annotation.surpriseLikelihood
            task_data["underExposedLikelihood"] = annotation.underExposedLikelihood
            task_data["blurredLikelihood"] = annotation.blurredLikelihood
            task_data["headwearLikelihood"] = annotation.headwearLikelihood
        elif task == "LANDMARK_DETECTION":
            task_data["description"] = annotation.description
            task_data["score"] = annotation.score
            task_data["location"] = annotation.locations
        elif task == "DOCUMENT_TEXT_DETECTION":
            task_data["description"] = annotation.description
        elif task == "OBJECT_LOCALIZATION":
            task_data["name"] = annotation.name
            task_data["score"] = annotation.score
        
        result.append(task_data)
    return result

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
                annotations = getattr(response, result)
                if annotations:
                    data[result] = getData(task, annotations)
    
    print("Results: ", data)
    return jsonify({"data": data})

if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)