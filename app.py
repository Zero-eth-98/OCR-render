import streamlit as st
from PIL import Image, UnidentifiedImageError
from pdf2image import convert_from_path
from docx import Document
import pytesseract
import uuid
import os

st.set_page_config(page_title="OCR Converter", layout="centered")
st.title("🧠 OCR Converter")
st.markdown("Carica **uno o più file** immagine o PDF. Il sistema rileverà automaticamente la lingua e ti permetterà di scaricare il risultato nel formato scelto.")

uploaded_files = st.file_uploader(
    "Trascina qui i file",
    type=["pdf", "png", "jpg", "jpeg", "webp", "bmp", "tiff", "tif", "pbm", "ppm"],
    accept_multiple_files=True
)

output_format = st.selectbox("📤 Seleziona formato di output", ("PDF", "TXT", "DOCX"))

# 👉 Bottone per avviare la conversione
if uploaded_files and st.button("🚀 Avvia OCR"):
    progress = st.progress(0)
    status = st.empty()
    preview = st.empty()

    for idx, file in enumerate(uploaded_files):
        file_ext = file.name.split('.')[-1].lower()
        temp_input = f"temp_{uuid.uuid4()}.{file_ext}"

        with open(temp_input, "wb") as f:
            f.write(file.read())

        text = ""
        images = []

        try:
            if file_ext == "pdf":
                images = convert_from_path(temp_input, dpi=200)
            else:
                img = Image.open(temp_input).convert("RGB")  # compressione automatica
                images = [img]

        except UnidentifiedImageError:
            st.error(f"❌ Impossibile aprire il file: {file.name}")
            continue

        total = len(images)
        for i, img in enumerate(images):
            text += pytesseract.image_to_string(img)
            percent = int(((idx + i / total) / len(uploaded_files)) * 100)
            progress.progress(percent)
            preview.text(f"📄 Anteprima testo ({file.name}): {text[:500]}...")

        file_base = f"{uuid.uuid4()}"

        if output_format == "PDF":
            pdf_output = f"{file_base}.pdf"
            images[0].save(pdf_output, save_all=True, append_images=images[1:])
            with open(pdf_output, "rb") as f:
                st.download_button(f"📥 Scarica PDF per {file.name}", f, file_name=f"{file.name}_output.pdf")
            os.remove(pdf_output)

        elif output_format == "TXT":
            txt_output = f"{file_base}.txt"
            with open(txt_output, "w", encoding="utf-8") as f:
                f.write(text)
            with open(txt_output, "rb") as f:
                st.download_button(f"📥 Scarica TXT per {file.name}", f, file_name=f"{file.name}_output.txt")
            os.remove(txt_output)

        elif output_format == "DOCX":
            doc = Document()
            doc.add_paragraph(text)
            docx_output = f"{file_base}.docx"
            doc.save(docx_output)
            with open(docx_output, "rb") as f:
                st.download_button(f"📥 Scarica DOCX per {file.name}", f, file_name=f"{file.name}_output.docx")
            os.remove(docx_output)

        os.remove(temp_input)

    progress.empty()
    status.success("✅ Tutti i file elaborati con successo!")
    preview.empty()
