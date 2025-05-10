import streamlit as st
import os
import uuid
import subprocess
from PIL import Image
import pytesseract
from langdetect import detect
from docx import Document
from pdf2image import convert_from_path

# Configurazione Tesseract per macOS
pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'
os.environ['TESSDATA_PREFIX'] = '/opt/homebrew/share/tessdata'

st.set_page_config(page_title="OCR PDF Converter", layout="centered")
st.title("📄 OCR PDF Converter")
st.write("Carica un'immagine o un PDF: riceverai un file PDF con testo selezionabile mantenendo il layout originale.")

uploaded_file = st.file_uploader("📎 Carica un file immagine o PDF", type=["pdf", "png", "jpg", "jpeg"])

if uploaded_file:
    file_ext = uploaded_file.name.split('.')[-1].lower()
    temp_input = f"{uuid.uuid4()}.{file_ext}"
    with open(temp_input, "wb") as f:
        f.write(uploaded_file.read())

    with st.spinner("🧠 Conversione OCR in corso..."):

        try:
            if file_ext in ["png", "jpg", "jpeg"]:
                # Converti immagine in PDF
                temp_pdf = f"{uuid.uuid4()}.pdf"
                subprocess.run(["img2pdf", temp_input, "-o", temp_pdf], check=True)

                # OCR invisibile su PDF generato
                output_pdf = f"{uuid.uuid4()}_ocr.pdf"
                subprocess.run([
                    "ocrmypdf",
                    "--language", "eng",
                    "--output-type", "pdfa",
                    "--skip-text",
                    temp_pdf,
                    output_pdf
                ], check=True)

                with open(output_pdf, "rb") as f:
                    st.success("✅ Conversione completata con successo!")
                    st.download_button("📥 Scarica PDF selezionabile", f, file_name="output.pdf")

                os.remove(temp_pdf)
                os.remove(output_pdf)

            elif file_ext == "pdf":
                # OCR diretto su PDF caricato
                output_pdf = f"{uuid.uuid4()}_ocr.pdf"
                subprocess.run([
                    "ocrmypdf",
                    "--language", "eng",
                    "--output-type", "pdfa",
                    "--skip-text",
                    temp_input,
                    output_pdf
                ], check=True)

                with open(output_pdf, "rb") as f:
                    st.success("✅ Conversione completata con successo!")
                    st.download_button("📥 Scarica PDF selezionabile", f, file_name="output.pdf")

                os.remove(output_pdf)

        except Exception as e:
            st.error(f"❌ Errore durante la conversione: {e}")

        finally:
            if os.path.exists(temp_input):
                os.remove(temp_input)

