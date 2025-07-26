from flask import render_template, request
from app import app
import pytesseract
import cv2
import os
import re
import numpy as np

# Path to Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

PAN_REGEX = r"[A-Z]{5}[0-9]{4}[A-Z]"

def preprocess_image(image_path):
    """Enhance image for better OCR."""
    img = cv2.imread(image_path)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Resize for consistency
    gray = cv2.resize(gray, (800, 600))

    # Optional: Sharpen the image
    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]])
    sharpened = cv2.filter2D(gray, -1, kernel)

    # Bilateral filter to reduce noise and keep edges
    filtered = cv2.bilateralFilter(sharpened, 11, 17, 17)

    # Adaptive thresholding
    thresh = cv2.adaptiveThreshold(filtered, 255,
                                   cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY, 15, 8)

    return thresh

def extract_text(image_path):
    processed_img = preprocess_image(image_path)
    config = "--oem 3 --psm 6"  # better layout understanding
    data = pytesseract.image_to_data(processed_img, config=config, output_type=pytesseract.Output.DICT)
    text = " ".join(data['text'])
    confidences = [int(conf) for conf in data['conf'] if conf != '-1']
    mean_conf = sum(confidences) / len(confidences) if confidences else 0
    return text, round(mean_conf, 2)

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    extracted_text = ""
    highlighted_text = ""
    if request.method == "POST":
        file = request.files.get("file_upload")
        if file:
            upload_path = app.config["UPLOADS"]
            os.makedirs(upload_path, exist_ok=True)
            filepath = os.path.join(upload_path, file.filename)
            file.save(filepath)

            extracted_text, confidence = extract_text(filepath)

            keywords = ['INCOME TAX DEPARTMENT', 'GOVT. OF INDIA', 'Permanent Account Number']
            score = sum(1 for word in keywords if word.lower() in extracted_text.lower())
            match = re.search(PAN_REGEX, extracted_text)

            if score >= 2 and match:
                pan = match.group()
                result = f"✅ Valid PAN Card Detected: {pan} (Confidence: {confidence}%)"
                highlighted_text = extracted_text.replace(pan, f"<mark>{pan}</mark>")
            else:
                result = f"❌ Invalid document: Not a PAN card. (Confidence: {confidence}%)"
                highlighted_text = extracted_text

    return render_template("index.html", pred=result, text=highlighted_text)
