import pymupdf


def extract_text(pdf_source: str) -> str:
    if isinstance(pdf_source, bytes):
        document = pymupdf.open(stream=pdf_source, filetype="pdf")
    else:
        document = pymupdf.open(pdf_source)

    with document:
        text = ""

        for page in document:
            text += page.get_text()

    return text
