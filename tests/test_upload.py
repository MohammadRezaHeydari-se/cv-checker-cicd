import pymupdf
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_upload_pdf():
    document = pymupdf.open()
    page = document.new_page()
    page.insert_text(
        (72, 72),
        "Name: Alex Smith\nEmail: alex@example.com\nSkills: Python"
    )

    pdf_bytes = document.tobytes()
    document.close()

    response = client.post(
        "/upload",
        files={
            "file": ("test_cv.pdf", pdf_bytes, "application/pdf")
        },
    )

    assert response.status_code == 200

    result = response.json()

    assert result["name"]["found"] is True
    assert result["email"]["found"] is True
    assert result["skills"]["found"] is True
    assert result["education"]["found"] is False

def test_upload_invalid_file():
    response = client.post(
        "/upload",
        files={
            "file": ("cv.txt", b"Hello World", "text/plain")
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid file type. Only PDF files are allowed."

def test_upload_large_file():
    large_file = b"x" * (5 * 1024 * 1024 + 1)

    response = client.post(
        "/upload",
        files={
            "file": ("large.pdf", large_file, "application/pdf")
        },
    )

    assert response.status_code == 413
    assert response.json()["detail"] == "PDF File is too large. 5 MB."
