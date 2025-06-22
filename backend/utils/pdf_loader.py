# backend/utils/pdf_loader.py
from PyPDF2 import PdfReader

def load_pdf_text_chunks(path: str, chunk_size=2000, overlap=400):
    reader = PdfReader(path)
    full_text = ""
    for page in reader.pages:
        full_text += page.extract_text() + "\n"

    # División con solapamiento
    chunks = []
    start = 0
    while start < len(full_text):
        end = start + chunk_size
        chunk = full_text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap

    return chunks
