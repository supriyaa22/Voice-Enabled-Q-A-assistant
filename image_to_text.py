import pytesseract
import cv2
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

def convert_image_to_text(path:str):
    img = Image.open(path)
    text= pytesseract.image_to_string(img)
    return text