from app.config.database import getSessionLocal
from app.models.model import PDF_Voyages


def createNewPDFVoyages(pdf_id,voyage_id):
    session= getSessionLocal()
    pdf_voyage = PDF_Voyages(
        pdf_id = pdf_id,
        voyage_id = voyage_id
    )
    session.add(pdf_voyage)
    session.commit()
    session.close()
    return pdf_voyage

def getPDFVoyagesByPDF_Id(pdf_id):
    session = getSessionLocal()
    pdf_Voyages = session.query(PDF_Voyages).filter_by(pdf_id = pdf_id).first()
    session.close()
    return pdf_Voyages

def getPDFVoyageByVoyage(voyage_id):
    session = getSessionLocal()
    pdf_Voyages = session.query(PDF_Voyages).filter_by(voyage_id = voyage_id).first()
    session.close()
    return pdf_Voyages