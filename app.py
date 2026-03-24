import streamlit as st
from PIL import Image, ImageOps
from utils import extract_text

# Page config
st.set_page_config(
    page_title="Handwritten OCR Pro",
    page_icon="✍️",
    layout="wide"
)

# Custom CSS
def inject_custom_css():
    css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
    }

    .main {
        background: linear-gradient(135deg, #0d1321, #1d2d44, #3e5c76) !important;
        color: #FFFFFF !important;
    }

    h1 {
        font-weight: 800 !important;
        font-size: 3rem !important;
        background: -webkit-linear-gradient(45deg, #00f2fe, #4facfe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
    }

    .custom-subheader {
        font-size: 1.5rem;
        font-weight: 600;
        color: #a8b2d1;
        text-align: center;
        margin-bottom: 20px;
    }

    .stTextArea textarea {
        background-color: #1a2332 !important;
        color: #e0e6ed !important;
        border-radius: 12px;
        padding: 15px;
    }

    .stFileUploader > div > div {
        border: 2px dashed #4facfe !important;
        border-radius: 16px !important;
        padding: 20px;
    }

    .stButton>button {
        background: linear-gradient(90deg, #11998e, #38ef7d) !important;
        color: white !important;
        border-radius: 12px !important;
        padding: 0.6rem 2rem !important;
        font-weight: 600 !important;
    }

    .stDownloadButton>button {
        background: linear-gradient(90deg, #FC466B, #3F5EFB) !important;
        color: white !important;
        border-radius: 12px !important;
    }

    /* Hide sidebar */
    section[data-testid="stSidebar"] {
        display: none;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

inject_custom_css()

# Title
st.markdown("<h1>✍️ Handwritten Multi-lingual OCR</h1>", unsafe_allow_html=True)
st.markdown("<p class='custom-subheader'>Digitize handwritten notes seamlessly across English, Hindi, and Bengali</p>", unsafe_allow_html=True)

# Layout
col1, space, col2 = st.columns([1, 0.1, 1])

# Upload Section
with col1:
    st.markdown("### 📤 Upload Note")
    
    uploaded_file = st.file_uploader(
        "Supported formats: PNG, JPG, JPEG",
        type=["png", "jpg", "jpeg"]
    )

    if uploaded_file is not None:
        image = Image.open(uploaded_file)

        # Fix rotation issue
        try:
            image = ImageOps.exif_transpose(image)
        except:
            pass

        st.image(image, caption="Uploaded Sample", width=350)

        st.markdown("<br>", unsafe_allow_html=True)

        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            extract_clicked = st.button("🚀 Extract Handwriting", use_container_width=True)

# Output Section
with col2:
    st.markdown("### 📝 Digitized Text Output")

    if uploaded_file is not None:
        if 'extract_clicked' in locals() and extract_clicked:
            with st.spinner("Analyzing handwriting..."):
                try:
                    # Default language = English
                    extracted_text = extract_text(image, "eng")

                    if not extracted_text.strip():
                        st.warning("No readable text found. Try a clearer image.")
                    else:
                        st.success("Extraction Completed!")
                        st.text_area("Your Copied Text:", extracted_text, height=350)

                        st.markdown("<br>", unsafe_allow_html=True)

                        st.download_button(
                            label="📥 Download as .TXT",
                            data=extracted_text,
                            file_name="extracted_text.txt",
                            mime="text/plain",
                            use_container_width=True
                        )

                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.info("Upload an image and click Extract.")
            st.text_area("Your Copied Text:", "", height=350, disabled=True)

    else:
        st.info("Awaiting file upload...")
        st.markdown(
            """
            <div style='background-color: #1a2332; padding: 20px; border-radius: 12px; text-align: center;'>
                🎨 <strong>Tips for better results:</strong><br><br>
                - Use clear handwriting<br>
                - Ensure good lighting<br>
                - Avoid tilted images
            </div>
            """,
            unsafe_allow_html=True
        )