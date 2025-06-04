from datetime import date

from app.services.aiService import *
from app.services.filePDFService import getAllPdf, getPDF
from app.services.manifestEntryService import save_manifest_entries
from app.services.pdfService import extract_text_with_plumber
from app.services.pdfToAiService import *
from app.services.testService import (getAllDataPDF, getDataPDF,
                                      insert_pdf_data, test_pdf_par_page)
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
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

# @router.post("/import")
# async def extract_pdf_data_with_ai(file: UploadFile = File(...)):
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

@router.post("/import")
async def extract_pdf_data_with_ai(
    file: UploadFile = File(...),
    start_page: int = Form(1),  # Valeur par défaut: 1
    end_page: Optional[int] = Form(None)  # Valeur par défaut: None (toutes les pages)
):
    try:
        # Lire et sauvegarder le PDF dans un dossier temporaire
        content = await file.read()
        
        # Créer le dossier s'il n'existe pas
        os.makedirs("pdfs", exist_ok=True)
        path = f"pdfs/{file.filename}"
        
        with open(path, "wb") as f:
            f.write(content)

        # Instancier PDFManager (sans DB) et créer un record temporaire
        manager = PDFManager(db_session=None, storage_dir="pdfs")
        reader = PdfReader(path)
        total_pages = len(reader.pages)
        
        # Si end_page n'est pas spécifié, traiter jusqu'à la dernière page
        if end_page is None:
            end_page = total_pages
        
        # Validation des paramètres
        if start_page < 1:
            raise HTTPException(status_code=400, detail="La page de début doit être supérieure à 0")
        
        if end_page < start_page:
            raise HTTPException(status_code=400, detail="La page de fin doit être supérieure ou égale à la page de début")
        
        if start_page > total_pages:
            raise HTTPException(
                status_code=400, 
                detail=f"La page de début ({start_page}) dépasse le nombre total de pages ({total_pages})"
            )
        
        if end_page > total_pages:
            end_page = total_pages  # Ajuster automatiquement à la dernière page

        record = FilePDF(
            nom=file.filename,
            pdf=content,
            date_ajout=date.today(),
            page=total_pages
        )

        # Instancier AIManager avec ta clé OpenAI
        ai = AIManager() 

        # Appeler l'analyse IA sur les pages spécifiées
        result = ai.analyze_pdf_pages(
            manager, 
            record, 
            start_page=start_page, 
            end_page=end_page, 
            mode="pdf"
        )
        print(result)
        # Sauvegarder    les entrées en base
        entries = save_manifest_entries(result, record)
        
        return {
            "success": True,
            "message": f"PDF traité avec succès (pages {start_page} à {end_page})",
            "total_pages": total_pages,
            "processed_pages": end_page - start_page + 1,
            "inserted": [e.to_dict() for e in entries],
            "total_entries": len(entries)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Erreur lors du traitement du PDF: {str(e)}"
        )
    finally:
        # Nettoyer le fichier temporaire (optionnel)
        try:
            if 'path' in locals() and os.path.exists(path):
                os.remove(path)
        except:
            pass

@router.post("/test")
def extract(file: UploadFile):
    return test_pdf_par_page(file)

@router.get("/get_test/{id}")
def testget(id : int):
    return getDataPDF(id)

@router.get("/get_all_data")
def get_All_PDF():
    return getAllDataPDF()

@router.get("/{id}")
async def get_pdf(id:int):
    pdf_stream = getPDF(id)
    if pdf_stream:
        return StreamingResponse(pdf_stream, media_type="application/pdf", headers={"Content-Disposition": f"inline; filename=file.pdf"})
    return {"error": "File not found"}


