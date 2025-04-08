from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import fitz  # PyMuPDF
import os
from pathlib import Path

app = FastAPI()

UPLOAD_DIR = "data/test_docs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload/")
async def upload_pdf(file: UploadFile = File(...)):
    file_location = Path(UPLOAD_DIR) / file.filename
    with open(file_location, "wb") as f:
        f.write(await file.read())

    text = extract_text_from_pdf(file_location)
    return JSONResponse(content={"filename": file.filename, "extracted_text": text[:1000]})

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    doc.close()
    return full_text