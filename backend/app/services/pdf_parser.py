import pdfplumber
from fastapi import UploadFile
import tempfile, os

async def extract_text(file: UploadFile) -> str:
    contents = await file.read()
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(contents)
        tmp_path = tmp.name

    text = ""
    with pdfplumber.open(tmp_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    os.unlink(tmp_path)
    return text