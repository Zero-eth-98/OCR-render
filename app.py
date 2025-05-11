import streamlit as st
import os
import uuid
import subprocess
from PIL import Image
import pytesseract
from langdetect import detect
from docx import Document
from pdf2image import convert_from_path
import img2pdf

# ✅ CONFIG STREAMLIT UI
st.set_page_config(
    page_title="SDB Tools – OCR Converter",
    page_icon="📄",
    layout="centered"
)

# ✅ STILE COERENTE CON SDBTOOLS
st.markdown("""
    <style>
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 700px;
        }
        .stButton>button {
            background-color: #0ea5e9;
            color: white;
            border: none;
            padding: 0.5rem 1.2rem;
            border-radius: 8px;
            font-size: 1rem;
        }
        .stButton>button:hover {
            background-color: #0284c7;
        }
        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# ✅ INTERFACCIA
st.title("🧠 OCR PDF Converter – SDB Tools")
st.write("Carica un'immagine o un PDF per estrarre testo selezionabile. Conversione diretta in PDF.")

# ✅ TESSERACT PATH
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
os.environ['TESSDATA_PREFIX'] = '/usr/share/tesseract-ocr/5/tessdata'

# ✅ UPLOAD FILE
uploaded_file = st.file_uploader("📎 Carica un file immagine o PDF", type=["pdf", "png", "jpg", "jpeg"])

# ✅ OCR
if uploaded_file:
    file_ext = uploaded_file.name.split('.')[-1].lower()
    temp_input = f"{uuid.uuid4()}.{file_ext}"
    with open(temp_input, "wb") as f:
        f.write(uploaded_file.read())

    with st.spinner("🧠 Conversione OCR in corso..."):
        try:
            if file_ext in ["png", "jpg", "jpeg"]:
                temp_pdf = f"{uuid.uuid4()}.pdf"
                with open(temp_pdf, "wb") as f:
                    f.write(img2pdf.convert(temp_input))
                input_pdf = temp_pdf
            else:
                input_pdf = temp_input

            output_pdf = f"{uuid.uuid4()}_ocr.pdf"

            subprocess.run([
                "ocrmypdf",
                "--language", "eng",
                "--output-type", "pdfa",
                input_pdf,
                output_pdf
            ], check=True)

            with open(output_pdf, "rb") as f:
                st.success("✅ Conversione completata con successo!")
                st.download_button("📥 Scarica PDF selezionabile", f, file_name="output.pdf")

        except subprocess.CalledProcessError as e:
            if e.returncode == 3:
                st.warning("ℹ️ Il PDF conteneva già testo, ma è stato comunque processato.")
                if os.path.exists(output_pdf):
                    with open(output_pdf, "rb") as f:
                        st.download_button("📥 Scarica PDF (testo già presente)", f, file_name="output.pdf")
            else:
                st.error(f"❌ Errore durante la conversione: {e}")

        except Exception as e:
            st.error(f"❌ Errore imprevisto: {e}")

        finally:
            for f in [temp_input, input_pdf, output_pdf]:
                if os.path.exists(f):
                    os.remove(f)
