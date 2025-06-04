from datetime import date

from app.services.aiService import *
from app.services.filePDFService import getAllPdf, getPDF
from app.services.manifestEntryService import (get_all_manifest_entries,
                                               save_manifest_entries)
from app.services.pdfService import extract_text_with_plumber
from app.services.pdfToAiService import *
from app.services.testService import (getAllDataPDF, getDataPDF,
                                      insert_pdf_data, test_pdf_par_page)
from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import StreamingResponse

router = APIRouter()

@router.get("/getAll")
async def getAllPDF():
    resultat = getAllPdf()
    
    files_info = []

    # Parcourir tous les documents
    for document in resultat:

        # Ajouter les informations du fichier à la liste
        files_info.append({
            "id": document.id,
            "nom": document.nom,
            "date_ajout":document.date_ajout,
            "nombre_page":document.page
        })
    return {"data":files_info}

@router.post("/import")
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
# async def extract(file: UploadFile):
#     return await insert_pdf_data(file)

@router.post("/test")
def extract(file: UploadFile):
    return test_pdf_par_page(file)

@router.get("/get_test/{id}")
def testget(id : int):
    return getDataPDF(id)

@router.get("/get_all_data")
def get_All_PDF():
    return get_all_manifest_entries()

@router.get("/{id}")
async def get_pdf(id:int):
    pdf_stream = getPDF(id)
    if pdf_stream:
        return StreamingResponse(pdf_stream, media_type="application/pdf", headers={"Content-Disposition": f"inline; filename=file.pdf"})
    return {"error": "File not found"}


