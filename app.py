import streamlit as st
import easyocr
import numpy as np
from PIL import Image

# Page config
st.set_page_config(page_title="Handwritten OCR", layout="wide")

# Remove sidebar completely
st.markdown("""
    <style>
        section[data-testid="stSidebar"] {display: none;}
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown(
    "<h1 style='text-align: center; color: #00BFFF;'>✍️ Handwritten Multi-lingual OCR</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align: center;'>Digitize handwritten notes seamlessly across English, Hindi, and Bengali</p>",
    unsafe_allow_html=True
)

# Layout
col1, space, col2 = st.columns([1, 0.1, 1])

# Load EasyOCR
@st.cache_resource
def load_model():
    return easyocr.Reader(['en', 'hi', 'bn'])

reader = load_model()

# Upload section
with col1:
    st.markdown("### 📤 Upload Note")
    uploaded_file = st.file_uploader(
        "Upload an image",
        type=["png", "jpg", "jpeg"]
    )

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, width=350)

# Output section
with col2:
    st.markdown("### 📝 Digitized Text Output")

    if uploaded_file is not None:
        with st.spinner("Processing..."):
            img_array = np.array(image)
            results = reader.readtext(img_array)

            extracted_text = " ".join([res[1] for res in results])

        st.success("Text Extracted Successfully!")
        st.text_area("Output", extracted_text, height=300)
    else:
        st.info("Awaiting file upload...")