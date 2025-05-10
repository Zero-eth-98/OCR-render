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

# Configura Tesseract per Render/macOS/Docker
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'  # o '/opt/homebrew/bin/tesseract' se locale Mac
os.environ['TESSDATA_PREFIX'] = '/usr/share/tesseract-ocr/5/tessdata'

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
                # Converti immagine in PDF con img2pdf
                temp_pdf = f"{uuid.uuid4()}.pdf"
                with open(temp_pdf, "wb") as f:
                    f.write(img2pdf.convert(temp_input))
                input_pdf = temp_pdf
            else:
                input_pdf = temp_input

            output_pdf = f"{uuid.uuid4()}_ocr.pdf"

            # OCR completo anche se il PDF ha già testo
            subprocess.run([
                "ocrmypdf",
                "--language", "eng",
                "--output-type", "pdfa",
                input_pdf,
                output_pdf
            ], check=True)

            # Mostra il PDF finale
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
            # Pulisci file temporanei
            for f in [temp_input, input_pdf, output_pdf]:
                if os.path.exists(f):
                    os.remove(f)
