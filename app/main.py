from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse

app =FastAPI()

HTML_FILE = Path(__file__).parent / "index.html"


@app.get("/")
def home():
    return FileResponse(HTML_FILE)

@app.get("/health")
def health():
    return {"status": "ok"}

