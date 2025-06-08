import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_bytes: bytes, filename: str) -> str:
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text