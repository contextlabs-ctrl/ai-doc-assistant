import PyPDF2
import docx
import requests
from bs4 import BeautifulSoup

class DocumentReader:
    @staticmethod
    def read_pdf(file):
        reader = PyPDF2.PdfReader(file)
        return "\n".join(page.extract_text() or "" for page in reader.pages)

    @staticmethod
    def read_txt(file):
        return file.read().decode("utf-8")

    @staticmethod
    def read_docx(file):
        doc = docx.Document(file)
        return "\n".join([para.text for para in doc.paragraphs])

    @staticmethod
    def fetch_url(url):
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')
        return ' '.join(p.get_text() for p in soup.find_all('p'))

    @staticmethod
    def extract_content(upload_type, input_data):
        if upload_type == "Upload File":
            if input_data.type == "application/pdf":
                return DocumentReader.read_pdf(input_data)
            elif input_data.type == "text/plain":
                return DocumentReader.read_txt(input_data)
            elif input_data.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                return DocumentReader.read_docx(input_data)
        elif upload_type == "Enter URL":
            return DocumentReader.fetch_url(input_data)
        return ""
