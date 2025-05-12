import streamlit as st
from PIL import Image, UnidentifiedImageError
from pdf2image import convert_from_path
from docx import Document
import pytesseract
import uuid
import os
import zipfile

st.set_page_config(page_title="OCR Converter", layout="centered")
st.title("🧠 OCR Converter")

st.markdown("Carica **uno o più file** immagine o PDF. Il sistema rileverà automaticamente la lingua e ti permetterà di scaricare il risultato nel formato scelto.")

uploaded_files = st.file_uploader(
    "Trascina qui i file o clicca per selezionare",
    type=["pdf", "png", "jpg", "jpeg", "webp", "bmp", "tiff", "tif", "pbm", "ppm"],
    accept_multiple_files=True
)

output_format = st.selectbox("📤 Seleziona formato di output", ("PDF", "TXT", "DOCX"))

if uploaded_files:
    st.subheader("📤 Caricamento file in corso...")
    load_bar = st.progress(0)

    for i in range(100):
        load_bar.progress(i + 1)

    st.success("✅ File caricati correttamente.")
    st.divider()

    if st.button("🚀 Scarica ora"):
        st.subheader("⚙️ Conversione in corso...")
        convert_bar = st.progress(0)

        output_paths = []
        total_files = len(uploaded_files)

        for idx, file in enumerate(uploaded_files):
            ext = file.name.split('.')[-1].lower()
            temp_input = f"temp_{uuid.uuid4()}.{ext}"
            with open(temp_input, "wb") as f:
                f.write(file.read())

            try:
                if ext == "pdf":
                    images = convert_from_path(temp_input, dpi=200)
                else:
                    img = Image.open(temp_input).convert("RGB")
                    images = [img]
            except UnidentifiedImageError:
                st.error(f"❌ Errore durante l'apertura del file: {file.name}")
                os.remove(temp_input)
                continue

            text = ""
            for img in images:
                text += pytesseract.image_to_string(img)

            output_base = f"{uuid.uuid4()}"
            out_path = ""

            if output_format == "PDF":
                out_path = f"{output_base}.pdf"
                images[0].save(out_path, save_all=True, append_images=images[1:])
            elif output_format == "TXT":
                out_path = f"{output_base}.txt"
                with open(out_path, "w", encoding="utf-8") as f:
                    f.write(text)
            elif output_format == "DOCX":
                out_path = f"{output_base}.docx"
                doc = Document()
                doc.add_paragraph(text)
                doc.save(out_path)

            output_paths.append(out_path)
            os.remove(temp_input)
            convert_bar.progress(int(((idx + 1) / total_files) * 100))

        st.success("✅ File convertiti con successo!")

        # ZIP se più file
        if len(output_paths) > 1:
            zip_name = f"ocr_result_{uuid.uuid4()}.zip"
            with zipfile.ZipFile(zip_name, 'w') as zipf:
                for file in output_paths:
                    zipf.write(file)
                    os.remove(file)
            with open(zip_name, "rb") as f:
                st.download_button("📦 Scarica ora", f, file_name="ocr_result.zip")
            os.remove(zip_name)
        else:
            file_path = output_paths[0]
            with open(file_path, "rb") as f:
                st.download_button("📥 Scarica ora", f, file_name=f"ocr_result.{output_format.lower()}")
            os.remove(file_path)

        convert_bar.empty()

