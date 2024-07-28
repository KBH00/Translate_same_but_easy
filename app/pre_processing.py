from paddleocr import PaddleOCR
import cv2
from matplotlib import pyplot as plt

def ocr_paddle(image_path):
    ocr = PaddleOCR(use_angle_cls=True, lang='en')
    result = ocr.ocr(image_path, cls=True)

    for line in result:
        print(line)

    image = cv2.imread(image_path)

    return result

def print_ocr(result):
    boxes = []
    texts = []
    scores = []

    for line in result:
        for word_info in line:
            bbox = word_info[0]
            text = word_info[1][0]
            score = word_info[1][1]
            boxes.append(bbox)
            texts.append(text)
            scores.append(score)
            print(f'Text: {text}, Score: {score}')

import fitz 

def extract_text_from_pdf(file_path):
    document = fitz.open(file_path)
    text = ''
    for page in document:
        text += page.get_text("text")
    return text

