from fastapi import APIRouter,Form,Request
from datetime import datetime
from app.services.rechercheService import search_in_contenu,search_pdf_name
from app.services.testService import searchPDFByVessel,searchPDFByVoyage,searchPDFByVoyageDate
router = APIRouter()


@router.get("/search_in_pdf")
def search_in_pdf(request:Request) :
    text = request._query_params.get("text")
    resultat = search_in_contenu(text)
    return resultat

@router.get("/search_pdf_name")
def search_pdf(request : Request):
    text = request._query_params.get("text")
    resultat = search_pdf_name(text)
    return {"resultat":resultat}

@router.get("/search_pdf_vessel")
def search_pdf_vessel(request: Request):
    text = request._query_params.get("text")
    resultat = searchPDFByVessel(text)
    return {"resultat":resultat}

@router.get("/search_pdf_voyage")
def search_pdf_voyage(request: Request):
    text = request._query_params.get("text")
    resultat = searchPDFByVoyage(text)
    return {"resultat":resultat}


@router.get("/search_entre_date")
def search_pdf_entre_date(request: Request):
    date_debut = request._query_params.get("date_debut")
    date_fin = request._query_params.get("date_fin")
    resultat = searchPDFByVoyageDate(date_debut = datetime.strptime(date_debut,"%Y-%m-%d"),date_fin= datetime.strptime(date_fin,"%Y-%m-%d"))
    return {"resultat":resultat}

