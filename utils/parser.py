import fitz

def parse_resume(file_path: str):
    with fitz.open(file_path) as pdf:
        text = ""
        for page in pdf:
            text += page.get_text()
    return text
