import pdfplumber
import re

class DocumentReader:
    @staticmethod
    def read_pdf(file):
        text = ""
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                content = page.extract_text()
                if content:
                    text += content + "\n"

        cleaned = DocumentReader.clean_pdf_text(text)
        return cleaned

    @staticmethod
    def clean_pdf_text(text):
        # Basic cleaning for academic or structured articles
        # Skip typical academic headers like abstract, keywords, references
        lines = text.split("\n")
        filtered = []

        skip_keywords = ["journal", "doi", "received", "abstract", "keywords", "references", "copyright"]
        end_keywords = ["references", "acknowledgment", "bibliography"]

        end_section = False
        for line in lines:
            lower_line = line.strip().lower()

            if any(k in lower_line for k in end_keywords):
                end_section = True

            if not end_section and not any(k in lower_line for k in skip_keywords):
                if len(line.strip()) > 0:
                    filtered.append(line.strip())

        return "\n".join(filtered)
