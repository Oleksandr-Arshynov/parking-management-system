import cv2
from paddleocr import PaddleOCR
import re
import matplotlib.pyplot as plt
import numpy as np

def validate_ukraine_plate(text):
    pattern = r'^[A-Z]{2}\d{4}[A-Z]{2}$'
    return bool(re.match(pattern, text))

# Extract license plate text using PaddleOCR
def get_plate_number(image):
    
    ocr = PaddleOCR(use_angle_cls=True, lang='en')
    #image = cv2.imread(image_path)

    # Check if the image is loaded correctly
    if image is None:
        print(f"Error: Image could not be loaded.")
        return None

    # OCR
    result = ocr.ocr(image)

    for line in result:
        for word_info in line:
            text = word_info[1][0]
            text = text.strip().replace('\n', '').replace(' ', '')

            if validate_ukraine_plate(text):
                print(f"Detected License Plate: {text}")
                return text
            return text
            #else:
            #    print(f"Invalid License Plate format: {text}")

    return None
