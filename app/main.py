from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse

from app.pdf_reader import extract_text
from app.cv_checker import check_cv

import pymupdf

import os

app =FastAPI()

HTML_FILE = Path(__file__).parent / "index.html"

APP_VERSION = os.getenv("APP_VERSION", "dev")

@app.get("/")
def home():
    return FileResponse(HTML_FILE)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/version")
def version():
    return {"version": APP_VERSION}

@app.post("/upload")
async def upload_cv(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF files are allowed.")

    pdf_bytes = await file.read(5 * 1024 * 1024 + 1)  # Read up to 5 MB + 1 byte to check size

    if len(pdf_bytes) > 5 * 1024 * 1024:  # 5 MB limit
        raise HTTPException(status_code=413, detail="PDF File is too large. 5 MB.")

    import pymupdf

    try:
        text = extract_text(pdf_bytes)
    except (ValueError, RuntimeError, pymupdf.FileDataError):
        raise HTTPException(status_code=400, detail="Invalid PDF file.",)

    return check_cv(text)
