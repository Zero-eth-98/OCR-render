import streamlit as st
from PIL import Image, UnidentifiedImageError
from pdf2image import convert_from_path
from docx import Document
import pytesseract
import uuid
import os
import io
import zipfile

st.set_page_config(page_title="OCR Converter", layout="centered")
st.title("🧠 OCR Converter")
st.markdown("Carica **uno o più file** immagine o PDF. Il sistema rileverà automaticamente la lingua e ti permetterà di scaricare il risultato nel formato scelto.")

uploaded_files = st.file_uploader(
    "Trascina qui i file o clicca per selezionarli",
    type=["pdf", "png", "jpg", "jpeg", "webp", "bmp", "tiff", "tif", "pbm", "ppm"],
    accept_multiple_files=True
)

output_format = st.selectbox("📤 Seleziona formato di output", ("PDF", "TXT", "DOCX"))

if uploaded_files:
    if st.button("🚀 Scarica ora"):
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            total_files = len(uploaded_files)
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
                        img = Image.open(temp_input).convert("RGB")
                        images = [img]
                except UnidentifiedImageError:
                    st.error(f"❌ Errore con il file: {file.name}")
                    continue

                for i, img in enumerate(images):
                    text += pytesseract.image_to_string(img)

                file_base = f"{uuid.uuid4()}"

                if output_format == "PDF":
                    output_filename = f"{file_base}.pdf"
                    images[0].save(output_filename, save_all=True, append_images=images[1:])
                elif output_format == "TXT":
                    output_filename = f"{file_base}.txt"
                    with open(output_filename, "w", encoding="utf-8") as f:
                        f.write(text)
                elif output_format == "DOCX":
                    output_filename = f"{file_base}.docx"
                    doc = Document()
                    doc.add_paragraph(text)
                    doc.save(output_filename)

                with open(output_filename, "rb") as f:
                    zip_file.writestr(f"{file.name}_output.{output_filename.split('.')[-1]}", f.read())

                os.remove(temp_input)
                os.remove(output_filename)

                st.progress(int((idx + 1) / total_files * 100))

        st.success("✅ File convertiti con successo!")
        st.download_button("📦 Scarica ora", zip_buffer.getvalue(), file_name="risultati_ocr.zip")
