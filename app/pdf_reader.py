import pymupdf


def extract_text(pdf_path: str) -> str:
    with pymupdf.open(pdf_path) as document:
        text = ""

        for page in document:
            text += page.get_text()

    return text
