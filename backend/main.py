from flask import Flask, jsonify, request
from flask_cors import CORS
from google.cloud import vision
from vertexai.generative_models import GenerativeModel, Part, Image
import magic

app = Flask(__name__)
CORS(app)

RESPONSE_TABLE = {
    'LABEL_DETECTION': 'label_annotations',
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
        elif task == "LANDMARK_DETECTION":
            task_data["description"] = annotation.description
            task_data["score"] = annotation.score
            task_data["latitude"] = annotation.locations[0].lat_lng.latitude
            task_data["longitude"] = annotation.locations[0].lat_lng.longitude
        elif task == "DOCUMENT_TEXT_DETECTION":
            task_data["description"] = annotation.description
        elif task == "OBJECT_LOCALIZATION":
            task_data["name"] = annotation.name
            task_data["score"] = annotation.score
        
        result.append(task_data)
    return result

def generateDescription(imageBytes, data):
    mime = magic.Magic(mime=True)
    mime_type = mime.from_buffer(imageBytes)
    print(mime_type)
    image_part = Part.from_image(Image.from_bytes(imageBytes))
    model = GenerativeModel("gemini-2.5-pro-exp-03-25")
    prompt = f"Please describe this image.  If you need some idea of what the image is, the following are tags that were generated by image recognition: {', '.join(data)}."
    description = model.generate_content([prompt, image_part])
    return description.text

@app.route("/get-image-description", methods=["POST"])
def getImageDescription() -> vision.EntityAnnotation:
    generateTask = False
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
        if task == "GENERATE_DESCRIPTION":
            generateTask = True
            continue
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

    if generateTask == True:
        generatedDescription = generateDescription(image_bytes, data)
        print("Description: ", generatedDescription)
        return jsonify({"description": generatedDescription, "data": data})
    else:
        return jsonify({"data": data})


if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)