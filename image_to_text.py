import re
import easyocr
from PIL import Image
import cv2
import numpy as np

# Load any image format using PIL and convert to OpenCV format
def load_image(image_path):
    pil_image = Image.open(image_path).convert("RGB")  # Convert to RGB
    return cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)  # Convert to OpenCV format

# Use a raw string (r"...") for Windows paths
image_path = r"D:\default_tts\nepali_text.png"

# Load the image
image = load_image(image_path)

# Initialize two OCR readers (one for Nepali, one for French)
reader_devanagari = easyocr.Reader(['hi', 'mr', 'ne', 'en'])  # Devanagari-compatible languages
reader_french = easyocr.Reader(['fr', 'en'])  # French-compatible languages

# Perform OCR using the Nepali reader first
text_dev = reader_devanagari.readtext(image, detail=0)

# If no Nepali text found, use the French reader
if not text_dev:
    text_fr = reader_french.readtext(image, detail=0)
    text = " ".join(set(text_fr))
else:
    text = " ".join(set(text_dev))

# Remove unwanted characters (Keeps only Devanagari and Latin characters)
cleaned_text = re.sub(r'[^\u0900-\u097F\u0000-\u007F\s]', '', text)

# Fix common OCR errors like 'garon' to 'garçon'
cleaned_text = cleaned_text.replace("garon", "garçon")

# Further refine text if necessary by checking for additional known OCR errors
cleaned_text = re.sub(r'\bgarcon\b', 'garçon', cleaned_text)  # Fix for 'garcon'

# Ensure no double spaces, trim extra spaces and join words properly
cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()

print("Cleaned Text:", cleaned_text)
