import cv2
import numpy as np
from PIL import Image
import easyocr
import streamlit as st

@st.cache_resource(show_spinner="Loading OCR Models... This might take a moment on first run.")
def load_ocr_model(lang_code):
    """
    Load EasyOCR reader. Uses caching to avoid reloading model for every image.
    """
    langs = [lang_code, 'en'] if lang_code != 'en' else ['en']
    return easyocr.Reader(langs, gpu=False)  # Set gpu=True if CUDA is available

def preprocess_image(image):
    """
    Converts PIL image to OpenCV format which EasyOCR expects.
    """
    img = np.array(image.convert('RGB'))
    # Optional enhancement: we could add contrast/sharpness here if needed, 
    # but EasyOCR handles varying illumination well.
    return img

def extract_text(image, language='eng'):
    lang_map = {
        'eng': 'en',
        'hin': 'hi',
        'ben': 'bn'
    }
    lang_code = lang_map.get(language, 'en')
    
    # Load the reader
    reader = load_ocr_model(lang_code)
    
    # Process image
    processed_img = preprocess_image(image)
    
    # Read text with EasyOCR (detail=0 returns only the text strings)
    results = reader.readtext(processed_img, detail=0, paragraph=True)
    
    extracted_text = "\n\n".join(results)
    return extracted_text