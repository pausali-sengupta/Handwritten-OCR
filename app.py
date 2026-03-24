import streamlit as st
from PIL import Image
import base64
from utils import extract_text

# Configure Streamlit page for a modern wide look
st.set_page_config(
    page_title="Handwritten OCR Pro",
    page_icon="✍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling via CSS
def inject_custom_css():
    css = """
    <style>
    /* Global Styles */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
    }

    /* Background and Headers */
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
        letter-spacing: -1px;
    }
    
    /* Text Inputs and Area styling */
    .stTextArea textarea {
        background-color: #1a2332 !important;
        color: #e0e6ed !important;
        border: 1px solid #3e5c76 !important;
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: border 0.3s ease;
    }

    .stTextArea textarea:focus {
        border: 1px solid #4facfe !important;
        box-shadow: 0 0 10px rgba(79, 172, 254, 0.5);
    }
    
    /* Upload Box */
    .stFileUploader > div > div {
        background-color: rgba(255,255,255,0.03) !important;
        border: 2px dashed #4facfe !important;
        border-radius: 16px !important;
        padding: 20px;
        transition: transform 0.2s, background-color 0.2s;
    }
    .stFileUploader > div > div:hover {
        background-color: rgba(255,255,255,0.06) !important;
        transform: scale(1.01);
    }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #11998e 0%, #38ef7d 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.6rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        box-shadow: 0 8px 15px rgba(56, 239, 125, 0.3) !important;
        transition: all 0.3s ease !important;
        cursor: pointer;
    }

    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 20px rgba(56, 239, 125, 0.4) !important;
        filter: brightness(1.1);
    }
    
    .stDownloadButton>button {
        background: linear-gradient(90deg, #FC466B 0%, #3F5EFB 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.6rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        box-shadow: 0 8px 15px rgba(63, 94, 251, 0.3) !important;
        transition: all 0.3s ease !important;
    }

    .stDownloadButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 20px rgba(63, 94, 251, 0.4) !important;
        filter: brightness(1.1);
    }

    /* Selectbox styling */
    .stSelectbox > div[data-baseweb="select"] {
        border-radius: 12px;
        background-color: #1a2332 !important;
        border: 1px solid #3e5c76 !important;
        color: white;
    }
    
    /* Custom subheader */
    .custom-subheader {
        font-size: 1.5rem;
        font-weight: 600;
        color: #a8b2d1;
        margin-bottom: 20px;
        text-align: center;
    }
    
    /* Metrics panel glassmorphism */
    div[data-testid="metric-container"] {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 10px 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }
    
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

inject_custom_css()

# Sidebar Setup
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/8150/8150370.png", width=100)
    st.markdown("## Configuration ✨")
    
    language_display = st.selectbox(
        "Detected Handwritten Language",
        ["English 🇬🇧", "Hindi 🇮🇳", "Bengali 🇧🇩/🇮🇳"]
    )
    
    # Map the display name to exact key for extract_text
    lang_mapping = {
        "English 🇬🇧": "eng",
        "Hindi 🇮🇳": "hin",
        "Bengali 🇧🇩/🇮🇳": "ben"
    }
    selected_language = lang_mapping[language_display]

    st.markdown("---")
    st.markdown("### 🛠 Technologies Used")
    st.markdown("- **EasyOCR**: Deep Learning based text recognition")
    st.markdown("- **Streamlit**: Interactive Web GUI")
    st.markdown("- **OpenCV**: Image preprocessing")
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.caption("Powered by Next-Gen Agentic OCR 🚀")


# Main Page Content
st.markdown("<h1>✍️ Handwritten Multi-lingual OCR</h1>", unsafe_allow_html=True)
st.markdown("<p class='custom-subheader'>Digitize handwritten notes seamlessly across English, Hindi, and Bengali</p>", unsafe_allow_html=True)

# Layout for columns
col1, space, col2 = st.columns([1, 0.1, 1])

with col1:
    st.markdown("### 📤 Upload Note")
    uploaded_file = st.file_uploader(
        "Supported formats: PNG, JPG, JPEG",
        type=["png", "jpg", "jpeg"]
    )

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        # Convert image properly based on EXIF to prevent rotation issues 
        try:
            from PIL import ImageOps
            image = ImageOps.exif_transpose(image)
        except Exception:
            pass
            
        st.image(image, caption="Uploaded Original Sample", use_column_width=True, clamp=True)
        
        # Center the extract button
        st.markdown("<br>", unsafe_allow_html=True)
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            extract_clicked = st.button("🚀 Extract Handwriting", use_container_width=True)

with col2:
    st.markdown("### 📝 Digitized Text Output")
    
    if uploaded_file is not None:
        if 'extract_clicked' in locals() and extract_clicked:
            with st.spinner("Analyzing strokes and extracting text... Please wait."):
                try:
                    extracted_text = extract_text(image, selected_language)
                    
                    if not extracted_text.strip():
                        st.warning("No readable text could be discerned. Please try an image with clearer handwriting.")
                    else:
                        st.success("Extraction Completed!")
                        st.text_area("Your Copied Text:", extracted_text, height=350)

                        st.markdown("<br>", unsafe_allow_html=True)
                        st.download_button(
                            label="📥 Download as .TXT",
                            data=extracted_text,
                            file_name=f"handwritten_digitized_{selected_language}.txt",
                            mime="text/plain",
                            use_container_width=True
                        )
                except Exception as e:
                    st.error(f"An error occurred during extraction: {e}")
        else:
            # Placeholder text area when not extracted
            st.info("Upload an image and hit **Extract** to view the digitized details here.")
            st.text_area("Your Copied Text:", "", height=350, disabled=True)
    else:
        st.info("Awaiting file upload...")
        st.markdown(
            """
            <div style='background-color: #1a2332; padding: 20px; border-radius: 12px; border: 1px dotted #3e5c76; text-align: center;'>
                🎨 <strong>Tips for better extraction:</strong><br><br>
                - Ensure good lighting<br>
                - Keep angles as straight as possible<br>
                - Crop borders if necessary
            </div>
            """, unsafe_allow_html=True
        )