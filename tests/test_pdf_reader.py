import pymupdf

from app.pdf_reader import extract_text


def test_extract_text(tmp_path):
    pdf_path = tmp_path / "test_cv.pdf"

    doc = pymupdf.open()
    page = doc.new_page()
    page.insert_text((72, 72), "Name: Alex Smith")
    doc.save(pdf_path)
    doc.close()

    result = extract_text(str(pdf_path))

    assert "Name: Alex Smith" in result
