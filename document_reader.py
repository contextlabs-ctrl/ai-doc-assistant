import requests
import pdfplumber
from docx import Document
from io import BytesIO
from bs4 import BeautifulSoup

class DocumentReader:
    @staticmethod
    def extract_content(input_type, source):
        if input_type == "Upload File":
            return DocumentReader._extract_from_uploaded(source)
        elif input_type == "Enter URL":
            return DocumentReader._extract_from_url(source)
        return ""

    @staticmethod
    def _extract_from_uploaded(uploaded_file):
        file_type = uploaded_file.type
        if file_type == "application/pdf":
            return DocumentReader._extract_pdf(uploaded_file)
        elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            return DocumentReader._extract_docx(uploaded_file)
        elif file_type == "text/plain":
            return uploaded_file.getvalue().decode('utf-8')
        return ""

    @staticmethod
    def _extract_pdf(file):
        content = ""
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                content += page.extract_text() or ""
        return content.strip()

    @staticmethod
    def _extract_docx(file):
        content = ""
        doc = Document(BytesIO(file.read()))
        for para in doc.paragraphs:
            content += para.text + "\n"
        return content.strip()

    @staticmethod
    def _extract_from_url(url):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        text = soup.get_text(separator='\n')
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        return "\n".join(lines)
