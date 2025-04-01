import pdfplumber
from docx import Document
from io import BytesIO
import requests
from bs4 import BeautifulSoup


class DocumentReader:
    @staticmethod
    def extract_content(input_type, source):
        if input_type == "Upload File":
            return DocumentReader._from_uploaded(source)
        elif input_type == "Enter URL":
            return DocumentReader._from_url(source)
        return ""

    @staticmethod
    def _from_uploaded(file):
        file_type = file.type
        if file_type == "application/pdf":
            return DocumentReader._read_pdf(file)
        elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            return DocumentReader._read_docx(file)
        elif file_type == "text/plain":
            return file.getvalue().decode("utf-8")
        else:
            return "Unsupported file format."

    @staticmethod
    def _read_pdf(file):
        try:
            text = ""
            with pdfplumber.open(file) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            return text.strip() or "No readable text found in PDF."
        except Exception as e:
            return f"Error reading PDF: {e}"

    @staticmethod
    def _read_docx(file):
        try:
            content = ""
            doc = Document(BytesIO(file.read()))
            for para in doc.paragraphs:
                content += para.text + "\n"
            return content.strip() or "No text found in DOCX."
        except Exception as e:
            return f"Error reading DOCX: {e}"

    @staticmethod
    def _from_url(url):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")
            lines = [line.strip() for line in soup.get_text(separator="\n").splitlines() if line.strip()]
            return "\n".join(lines)
        except Exception as e:
            return f"Error fetching or parsing URL: {e}"
