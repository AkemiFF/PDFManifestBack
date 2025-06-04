from app.services.filePDFService import getAllPdf
from fastapi import UploadFile,File,APIRouter,HTTPException
from app.services.filePDFService import getPDF
from fastapi.responses import StreamingResponse
from app.services.testService import insert_pdf_data,getDataPDF,test_pdf_par_page,getAllDataPDF
from app.services.pdfService import extract_text_with_plumber

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
async def extract(file: UploadFile):
    return await insert_pdf_data(file)

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


