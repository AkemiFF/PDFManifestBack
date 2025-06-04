
import os
import warnings
from typing import List, Optional

import pdfplumber
from PyPDF2 import PdfReader, PdfWriter
from sqlalchemy.orm import Session

from app.models.model import FilePDF


class PDFManager:
    """
    Service class to manage FilePDF records and PDF operations:
    - list PDFs in DB
    - export a specific page as standalone PDF
    - extract raw text or structured content (including tables)
    - save new PDF records to DB
    """

    def __init__(self, db_session: Session, storage_dir: str = "pdfs"):
        self.db = db_session
        self.storage_dir = storage_dir
        os.makedirs(self.storage_dir, exist_ok=True)

    def list_pdfs(self) -> List[FilePDF]:
        return self.db.query(FilePDF).order_by(FilePDF.date_ajout.desc()).all()

    def save_pdf(self, name: str, binary_data: bytes, date_ajout, page_count: int) -> FilePDF:
        path = os.path.join(self.storage_dir, name)
        with open(path, "wb") as f:
            f.write(binary_data)
        file_pdf = FilePDF(nom=name, pdf=binary_data, date_ajout=date_ajout, page=page_count)
        self.db.add(file_pdf)
        self.db.commit()
        self.db.refresh(file_pdf)
        return file_pdf

    def get_file_path(self, record: FilePDF) -> str:
        return os.path.join(self.storage_dir, record.nom)

    def export_page_as_pdf(self, pdf_record: FilePDF, page_number: int, output_path: Optional[str] = None) -> str:
        path = self.get_file_path(pdf_record)
        reader = PdfReader(path)
        if page_number < 1 or page_number > len(reader.pages):
            raise ValueError(f"Page {page_number} out of range")
        writer = PdfWriter()
        writer.add_page(reader.pages[page_number - 1])
        if output_path is None:
            base, _ = os.path.splitext(pdf_record.nom)
            output_path = os.path.join(self.storage_dir, f"{base}_page{page_number}.pdf")
        with open(output_path, "wb") as f:
            writer.write(f)
        return output_path

    def extract_page_text(self, pdf_record: FilePDF, page_number: int) -> str:
        path = self.get_file_path(pdf_record)
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", message="CropBox missing.*")
            with pdfplumber.open(path) as pdf:
                if page_number < 1 or page_number > len(pdf.pages):
                    raise ValueError(f"Page {page_number} out of range")
                return pdf.pages[page_number - 1].extract_text() or ""

    def extract_structured(self, pdf_record: FilePDF, page_number: int) -> dict:
        path = self.get_file_path(pdf_record)
        data = {"text_blocks": [], "tables": []}
        with pdfplumber.open(path) as pdf:
            if page_number < 1 or page_number > len(pdf.pages):
                raise ValueError(f"Page {page_number} out of range")
            page = pdf.pages[page_number - 1]
            # collect text blocks
            for block in page.extract_words():
                data["text_blocks"].append(block)
            # collect tables
            for table in page.extract_tables():
                data["tables"].append(table)
        return data
