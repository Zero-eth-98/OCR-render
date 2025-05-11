# 🧠 OCR Converter – SDB Tools

Benvenuto nel repository ufficiale del progetto **OCR Converter** di [sdbtools.xyz](https://sdbtools.xyz). Questo strumento permette di **estrarre testo selezionabile da immagini e PDF**, direttamente dal browser, senza installazioni.

> 🚀 Realizzato in **Python + Streamlit**, e ottimizzato per il deploy su **Render** tramite Docker.

---

## 🔧 Funzionalità attualmente implementate

### ✅ Multi-upload con drag & drop
- Puoi caricare **uno o più file** contemporaneamente (PDF o immagini).

### ✅ Estensione formati in input
- Supporta: `pdf`, `png`, `jpg`, `jpeg`, `webp`, `bmp`, `tiff`, `tif`, `pbm`, `ppm`

### ✅ Selezione formato in output
- Output selezionabile: `PDF`, `TXT`, `DOCX`

### ✅ Rilevamento automatico lingua OCR
- Nessuna selezione manuale: la lingua del testo viene identificata automaticamente.

### ✅ Compressione e ottimizzazione immagini
- Tutte le immagini vengono convertite in `RGB` per una resa OCR ottimale.

### ✅ Anteprima testo OCR
- Per ogni file processato viene mostrata un'anteprima dei primi **500 caratteri** estratti.

### ✅ Barra di avanzamento e feedback
- Stato di progresso visivo e messaggi di stato durante la conversione.

### ✅ Download file processati
- I file convertiti sono disponibili per il download immediato, uno per uno.

---

## 🌐 Infrastruttura e deploy

- **Deploy** attuale su [Render](https://render.com) (free plan) usando `render.yaml` e `Dockerfile`
- **Dominio** personalizzato: `ocr.sdbtools.xyz` collegato tramite DNS su Namecheap
- **Email aziendali gratuite** gestite via Zoho Mail, in attesa di possibile upgrade a Google Workspace
- **Google Analytics 4** attivo per tracciare le sessioni e ottimizzare il comportamento utenti
- **Google AdSense** configurato per monetizzazione automatica e manuale, in attesa di attivazione definitiva
- **Indicizzazione** gestita con sitemap, robots.txt e Search Console per migliorare il posizionamento SEO

---

## 🌍 VPS e scalabilità futura

- L'app è attualmente ospitata su Render per rapidità di sviluppo
- La migrazione futura su **VPS (es. Hetzner o Contabo)** permetterà:
  - Maggiore potenza e performance
  - Accesso completo a log, file temporanei, e GPU se richiesto
  - Hosting multi-app sotto `sdbtools.xyz` (es: `pdf.sdbtools.xyz`, `img.sdbtools.xyz`, ecc.)
  - Gestione API OCR automatizzate e protezione con accesso autenticato

---

## 🌐 Tecnologie utilizzate
- `Python`
- `Streamlit`
- `pytesseract`
- `pdf2image`, `Pillow`
- `python-docx`, `reportlab`
- `uuid`, `langdetect`
- `Docker`, `Render.com`

---

## 🚀 Come eseguire in locale

```bash
# Clona il repository
$ git clone https://github.com/Zero-eth-98/OCR-render.git
$ cd OCR-render

# Installa le dipendenze
$ pip install -r requirements.txt

# Avvia il server
$ streamlit run app.py
```

> 📦 Se vuoi buildare un'immagine Docker:
```bash
docker build -t ocr-render .
docker run -p 8501:8501 ocr-render
```

---

## 🗺️ Roadmap funzionalità future
- [ ] ✨ **Conversione batch con ZIP** in uscita
- [ ] ▶️ Supporto a formati immagine HEIC/AVIF
- [ ] 🔍 Pulsante per **visualizzare testo completo**
- [ ] 📃 Log sessione OCR o salvataggio storico conversioni
- [ ] 🌍 Deploy su VPS con dominio primario (no Render)
- [ ] 🔐 Modalità accesso admin e gestione API OCR
- [ ] 🧠 Auto-rilevamento lingua avanzato con AI
- [ ] 📈 Dashboard statistiche utenti via Google Analytics
- [ ] 💸 Gestione dinamica annunci via AdSense in base a tool/lingua

---

## ✨ Progetto parte della suite [sdbtools.xyz](https://sdbtools.xyz)

Questa è una delle web app ufficiali del portale **SDB Tools**, che raccoglie strumenti gratuiti per PDF, immagini, video, audio e altro.

Altri strumenti in arrivo:
- PDF merge/split/compression
- Video to MP3
- Image Optimizer
- Audio Editor online

---

## 🛡️ Licenza

Questo progetto è rilasciato sotto **MIT License**. Libero utilizzo e distribuzione con attribuzione.

---

## 🙏 Ringraziamenti
Grazie a tutte le librerie open source che rendono questo progetto possibile, in particolare:
- Tesseract OCR
- Streamlit
- OpenCV/Pillow

> Per feedback, segnalazioni bug o collaborazione: [contattaci](mailto:info@sdbtools.xyz)
