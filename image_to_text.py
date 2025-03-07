import easyocr
from PIL import Image
import cv2
import numpy as np
import re

# Load any image format using PIL and convert to OpenCV format
def load_image(image_path):
    pil_image = Image.open(image_path).convert("RGB")  # Convert to RGB
    return cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)  # Convert to OpenCV format

# Function to get the best text with the highest probability
def get_best_text(results):
    if not results:
        return None, 0  # No text found
    results.sort(key=lambda x: x[2], reverse=True)  # Sort by confidence (highest first)
    
    # Combine detected words into a full sentence while preserving order
    sorted_by_position = sorted(results, key=lambda x: (x[0][1][1], x[0][0][0]))  # Sort by y, then x position
    sentence = " ".join([res[1] for res in sorted_by_position])
    
    return sentence, results[0][2]  # Return the full text and highest confidence

# Use a raw string (r"...") for Windows paths
image_path = r"D:\Image_To_Text\CHINEASE.png"

# Load the image
image = load_image(image_path)

# Initialize OCR readers for Chinese, Nepali, French, and English
reader_chinese = easyocr.Reader(['ch_tra', 'en'])  # Chinese OCR
reader_nepali = easyocr.Reader(['hi', 'mr', 'ne', 'en'])  # Nepali OCR
reader_french = easyocr.Reader(['fr', 'en'])  # French OCR
reader_english = easyocr.Reader(['en'])  # English OCR

# Step 1: Run OCR on all four languages
text_chinese_results = reader_chinese.readtext(image)
text_nepali_results = reader_nepali.readtext(image)
text_french_results = reader_french.readtext(image)
text_english_results = reader_english.readtext(image)

# Get best results for each language
best_chinese, conf_chinese = get_best_text(text_chinese_results)
best_nepali, conf_nepali = get_best_text(text_nepali_results)
best_french, conf_french = get_best_text(text_french_results)
best_english, conf_english = get_best_text(text_english_results)

# Determine the best result overall
best_text = None
best_confidence = 0
best_language = None

if best_chinese and conf_chinese > best_confidence:
    best_text, best_confidence, best_language = best_chinese, conf_chinese, "Chinese"

if best_nepali and conf_nepali > best_confidence:
    best_text, best_confidence, best_language = best_nepali, conf_nepali, "Nepali"

if best_french and conf_french > best_confidence:
    best_text, best_confidence, best_language = best_french, conf_french, "French"

if best_english and conf_english > best_confidence:
    best_text, best_confidence, best_language = best_english, conf_english, "English"

# Print the best result
if best_text:
    print(f"Extracted Text ({best_language} - Confidence {best_confidence:.2f}): {best_text}")
else:
    print("Extracted Text: Not Available")
