FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-all \  # installa tutte le lingue disponibili
    ghostscript \
    qpdf \
    poppler-utils \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libjpeg-dev \
    zlib1g-dev \
    libtiff-dev \
    libopenjp2-7 \
    libwebp-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set environment
ENV PYTHONUNBUFFERED=1
ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/5/tessdata

# Create app directory
WORKDIR /app
COPY . /app

# Install Python packages
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install ocrmypdf

# Expose Streamlit port
EXPOSE 8501

# Run the app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]