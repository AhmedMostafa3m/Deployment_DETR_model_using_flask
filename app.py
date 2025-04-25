from flask import Flask, render_template, request, redirect, url_for
import os
import cv2
import numpy as np
from PIL import Image
from transformers import DetrImageProcessor, DetrForObjectDetection
import torch
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load pre-trained DETR model and processor
processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50")
model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50")
model.eval()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_image(image_path):
    # Load image
    image = Image.open(image_path).convert("RGB")
    image_np = np.array(image)

    # Prepare image for DETR
    inputs = processor(images=image, return_tensors="pt")
    
    # Run inference
    with torch.no_grad():
        outputs = model(**inputs)
    
    # Post-process results
    target_sizes = torch.tensor([image.size[::-1]])
    results = processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=0.9)[0]
    
    # Draw bounding boxes and labels
    image_cv = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
    for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
        box = [int(i) for i in box.tolist()]
        label_str = model.config.id2label[label.item()]
        score_str = f"{score.item():.2f}"
        # Draw rectangle and text
        cv2.rectangle(image_cv, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2)
        cv2.putText(image_cv, f"{label_str} {score_str}", (box[0], box[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    # Save processed image
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'processed_' + os.path.basename(image_path))
    cv2.imwrite(output_path, image_cv)
    
    return os.path.basename(output_path)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Process the image
        processed_filename = process_image(file_path)
        
        return render_template('result.html', original=filename, processed=processed_filename)
    return redirect(request.url)

if __name__ == '__main__':
    app.run(debug=True)