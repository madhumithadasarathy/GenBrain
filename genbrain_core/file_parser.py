from pypdf import PdfReader
import io

def extract_text_from_file(file_content, filename):
    if filename.endswith(".pdf"):
        reader = PdfReader(io.BytesIO(file_content))
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    elif filename.endswith(".txt") or filename.endswith(".md"):
        return file_content.decode("utf-8")
    else:
        raise ValueError("Unsupported file format")
