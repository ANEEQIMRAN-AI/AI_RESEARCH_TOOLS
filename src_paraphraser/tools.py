# tools.py
import PyPDF2

def extract_text_from_pdf(uploaded_file):
    reader = PyPDF2.PdfReader(uploaded_file)
    return "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])

def count_words(text):
    return len(text.split()) if text else 0