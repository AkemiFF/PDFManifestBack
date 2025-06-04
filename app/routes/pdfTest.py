from datetime import date

from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import StreamingResponse

from app.services.aiService import *
from app.services.filePDFService import getAllPdf, getPDF
from app.services.manifestEntryService import save_manifest_entries
from app.services.pdfService import extract_text_with_plumber
from app.services.pdfToAiService import *

router = APIRouter()

import json
from datetime import date

from fastapi import APIRouter, File, UploadFile

router = APIRouter()

@router.post("/extract")
async def extract_text_from_uploaded_pdf(file: UploadFile = File(...)):
    # Lire le fichier
    content = await file.read()

    # Définir chemin de stockage temporaire
    tmp_dir = "pdfs"
    os.makedirs(tmp_dir, exist_ok=True)
    path = os.path.join(tmp_dir, file.filename)

    # Sauvegarder le fichier pour que PDFManager puisse y accéder
    with open(path, "wb") as f:
        f.write(content)

    # Initialiser PDFManager
    manager = PDFManager(db_session=None, storage_dir=tmp_dir)

    # Compter les pages
    reader = PdfReader(path)
    page_count = len(reader.pages)

    # Créer un objet temporaire
    temp_pdf = FilePDF(
        nom=file.filename,
        pdf=content,
        date_ajout=date.today(),
        page=page_count
    )

    # Extraire le texte page par page
    result = {}
    for i in range(1, page_count + 1):
        result[f"page_{i}"] = manager.extract_page_text(temp_pdf, i)

    return result





@router.post("/ai-extract")
async def extract_pdf_data_with_ai(file: UploadFile = File(...)):
    # Lire et sauvegarder le PDF dans un dossier temporaire
    content = await file.read()
    path = f"pdfs/{file.filename}"
    with open(path, "wb") as f:
        f.write(content)

    # Instancier PDFManager (sans DB) et créer un record temporaire
    manager = PDFManager(db_session=None, storage_dir="pdfs")
    reader = PdfReader(path)
    record = FilePDF(
        nom=file.filename,
        pdf=content,
        date_ajout=date.today(),
        page=len(reader.pages)
    )

    # Instancier AIManager avec ta clé OpenAI
    ai = AIManager() 

    # Appeler l’analyse IA sur toutes les pages
    result = ai.analyze_pdf_pages(manager, record, start_page=1, end_page=3, mode="pdf")

    entries = save_manifest_entries(result)
    return {"inserted": [e.to_dict() for e in entries]}

@router.post("/ai-save")
async def extract_pdf_data_with_ai(file: UploadFile = File(...)):
    # Lire et sauvegarder le PDF dans un dossier temporaire
    content = await file.read()
    path = f"pdfs/{file.filename}"
    with open(path, "wb") as f:
        f.write(content)

    # Instancier PDFManager (sans DB) et créer un record temporaire
    manager = PDFManager(db_session=None, storage_dir="pdfs")
    reader = PdfReader(path)
    record = FilePDF(
        nom=file.filename,
        pdf=content,
        date_ajout=date.today(),
        page=len(reader.pages)
    )

    # Instancier AIManager avec ta clé OpenAI
    ai = AIManager() 

    # Appeler l’analyse IA sur toutes les pages
    result = [
        {
            "Name": "KOUROS QUEEN",
            "Flag": "PANAMA",
            "Produits": "Ordinary Portland Cement (OPC)",
            "Volume": None,
            "Poids": 9000000,
            "DATE": "2024-12-18"
        },
        {
            "Name": "KOUROS QUEEN",
            "Flag": "PANAMA",
            "Produits": "Ordinary Portland Cement (OPC)",
            "Volume": None,
            "Poids": 8000000,
            "DATE": "2024-12-18"
        },
        {
            "Name": "KOUROS QUEEN",
            "Flag": "PANAMA",
            "Produits": "Ordinary Portland Cement (OPC)",
            "Volume": None,
            "Poids": 7000000,
            "DATE": "2024-12-18"
        },
        {
            "Name": "KOUROS QUEEN",
            "Flag": "PANAMA",
            "Produits": "Ordinary Portland Cement (OPC)",
            "Volume": None,
            "Poids": 6000000,
            "DATE": "2024-12-18"
        },
        {
            "Name": "KOUROS QUEEN",
            "Flag": "PANAMA",
            "Produits": "Ordinary Portland Cement (OPC)",
            "Volume": None,
            "Poids": 3328000,
            "DATE": "2024-12-18"
        },
        {
            "Name": "KOUROS QUEEN",
            "Flag": "PANAMA",
            "Produits": "Ordinary Portland Cement (OPC)",
            "Volume": None,
            "Poids": 1000000,
            "DATE": "2024-12-18"
        }
        ]
    
    entries = save_manifest_entries(result)
    return {"inserted": [e.to_dict() for e in entries]}