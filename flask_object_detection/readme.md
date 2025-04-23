I’ll guide you through creating a Flask web application on Windows that uses a pre-trained object detection model to detect objects in an uploaded image, draw bounding boxes, and classify the objects. We’ll use a pre-trained model from the `transformers` library (e.g., DETR, a popular object detection model) and OpenCV for drawing bounding boxes. The app will allow users to upload an image, process it, and display the results with bounding boxes and labels.

The app will:
- Have a homepage for uploading an image.
- Process the image using a pre-trained DETR model.
- Draw bounding boxes and labels on the image using OpenCV.
- Display the processed image with detected objects.

### **Steps to Create the Flask Object Detection Web App**

#### **1. Prerequisites**
- Ensure **Python 3.8 or higher** is installed. Download from [python.org](https://www.python.org/downloads/) if needed.
- Install **Git** for Windows (optional, for cloning repositories): [git-scm.com](https://git-scm.com/download/win).
- Have a text editor like VS Code or Notepad++ for editing code.

#### **2. Set Up the Project Environment**
1. **Create a Project Directory**:
   - Open a Command Prompt (cmd) or PowerShell.
   - Create and navigate to a project directory:
     ```bash
     mkdir flask_object_detection
     cd flask_object_detection
     ```

2. **Set Up a Virtual Environment**:
   - Create a virtual environment:
     ```bash
     python -m venv venv
     ```
   - Activate it:
     ```bash
     venv\Scripts\activate
     ```
     You should see `(venv)` in your prompt.

3. **Install Dependencies**:
   - Install Flask, OpenCV, Pillow, NumPy, Torch, and the `transformers` library:
     ```bash
     pip install flask opencv-python pillow numpy torch torchvision transformers
     ```
   - Note: `torch` and `torchvision` are required for the DETR model. If you have a GPU and want to use it, ensure you install the GPU-compatible version of PyTorch (check [pytorch.org](https://pytorch.org/get-started/locally/) for Windows instructions).

#### **3. Create the Project Structure**
- Inside `flask_object_detection`, create the following structure:
  ```
  flask_object_detection/
  ├── static/
  │   ├── uploads/           # Store uploaded and processed images
  │   └── css/
  │       └── style.css     # Basic CSS for styling
  ├── templates/
  │   ├── index.html        # Homepage with upload form
  │   └── result.html       # Display processed image
  ├── app.py                # Flask app logic
  └── venv/                 # Virtual environment
  ```
- Create the `static/uploads` and `static/css` folders manually using File Explorer or the command line:
  ```bash
  mkdir static static\uploads static\css
  mkdir templates
  ```

#### **4. Write the Code**
Below are the files names for the Flask app. these apps are located as mentioned in the app structure, The app uses the `facebook/detr-resnet-50` model from Hugging Face’s `transformers` for object detection, processes the image with OpenCV to draw bounding boxes, and serves the result via Flask.

* app.py
* index.html
* result.html
* style.css

#### **5. Run the Application**
1. **Ensure the Virtual Environment is Activated**:
   ```bash
   venv\Scripts\activate
   ```

2. **Set Flask Environment Variables**:
   ```bash
   set FLASK_APP=app.py
   set FLASK_ENV=development
   ```

3. **Run the Flask App**:
   ```bash
   flask run
   ```
   - If you encounter issues, try running directly:
     ```bash
     python app.py
     ```

4. **Access the App**:
   - Open a browser and go to `http://127.0.0.1:5000`.
   - Upload a `.jpg`, `.jpeg`, or `.png` image, and the app will display the original and processed images with bounding boxes and labels.

#### **6. Test the App**
- Upload an image containing objects (e.g., people, cars, animals).
- The app will:
  - Detect objects using the DETR model (confidence threshold set to 0.9 for clarity).
  - Draw green bounding boxes with labels and confidence scores.
  - Save the processed image in `static/uploads` with a `processed_` prefix.
  - Display both the original and processed images on the result page.
- Click “Upload Another Image” to try again.

### **Explanation of the Code**
- **app.py**:
  - Initializes a Flask app and configures an upload folder.
  - Loads the `facebook/detr-resnet-50` model and processor for object detection.
  - Defines routes:
    - `/`: Renders the upload form (`index.html`).
    - `/upload` (POST): Handles image uploads, checks file extensions, processes the image, and renders `result.html`.
  - The `process_image` function:
    - Loads the image using PIL.
    - Processes it with DETR to get bounding boxes, labels, and scores.
    - Uses OpenCV to draw bounding boxes and labels.
    - Saves the processed image and returns its filename.
- **index.html**:
  - A simple form for uploading images, styled with CSS.
- **result.html**:
  - Displays the original and processed images side by side with a link to upload another image.
- **style.css**:
  - Basic styling for a clean, responsive UI.

### **Additional Notes**
- **Model Choice**: The `facebook/detr-resnet-50` model is lightweight and effective for general object detection (trained on COCO dataset). For specific use cases, you can swap it with other models like YOLO (requires additional setup).
- **Performance**:
  - The first inference may be slow due to model loading. Subsequent requests are faster.
  - If you have a GPU, ensure PyTorch is GPU-compatible for faster processing.
- **File Handling**:
  - Only `.jpg`, `.jpeg`, and `.png` files are allowed.

- **Storage**:
  - Images are saved in `static/uploads`. In production, consider cleaning up old files or using a database.
  
### **Example Usage**
- Upload an image of a street scene (e.g., cars, people, traffic signs).
- The app might detect “car” (score: 0.95), “person” (score: 0.92), etc., and draw green boxes with labels.
- The result page shows the original image and the processed image with annotations.

```
![bus](https://github.com/user-attachments/assets/cb060f52-0f78-4dd0-ba17-1769c4d29b44)

```
