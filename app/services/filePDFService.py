from app.config.database import getSessionLocal
from app.models.model import FilePDF
import io
from datetime import date

def getAllPdf():
    session = getSessionLocal()
    filePdf =  session.query(FilePDF).all()
    session.close()
    return filePdf

def createNewFilePDF(nom,pdf,page):
    session = getSessionLocal()
    today = date.today()
    newFilePDF = FilePDF(
        nom = nom,
        pdf = pdf,
        date_ajout = today,
        page = page
    )
    session.add(newFilePDF)
    session.commit()
    session.refresh(newFilePDF)
    return newFilePDF

def getById(id):
    session = getSessionLocal()
    filePDF = session.query(FilePDF).filter_by(id = id).first()
    session.close()
    return filePDF

def getPDF(id):
    session = getSessionLocal()
    filePDF = session.query(FilePDF).filter_by(id = id).first()
    file_stream = io.BytesIO(filePDF.pdf)
    session.close()
    return file_stream