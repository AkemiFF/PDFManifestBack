from app.config.database import getSessionLocal
from app.services.rechercheService import sont_presque_pareils
from app.models.model import Voyage
from datetime import datetime

def getAllVoyage():
    session = getSessionLocal()
    voyages = session.query(Voyage).all()
    session.close()
    return voyages

def getVoyageByCode(code) : 
    session = getSessionLocal()
    voyage = session.query(Voyage).filter_by(code = code).first()
    session.close()
    return voyage

def getVoyageById(id) :
    session = getSessionLocal()
    voyage = session.query(Voyage).filter_by(id = id).first()
    session.close()
    return voyage

def getVoyageByVessel(vessel_id):
    session = getSessionLocal()
    voyages = session.query(Voyage).filter_by(vessel_id = vessel_id).all()
    session.close()
    return voyages    

def createNewVoyage(code,date_arrive,vessel_id):
    session = getSessionLocal()
    newVoyage = Voyage(code = code,date_arrive = date_arrive,vessel_id = vessel_id)
    session.add(newVoyage)
    session.commit()
    session.refresh(newVoyage)
    session.close()
    return newVoyage

def getAllVoyageByDate(date_arrive):
    session = getSessionLocal()
    voyages = session.query(Voyage).filter_by(date_arrive = date_arrive).all()
    session.close()
    return voyages


def getOrCreateVoyage(code,vessel_id,date_arrive):
    voyage = getVoyageByCode(code)
    if not voyage :
        voyage = createNewVoyage(
            code= code,
            date_arrive= datetime.strptime(date_arrive, "%Y-%m-%d").date(),
            vessel_id= vessel_id
        )

    return voyage

def search_voyage_name(text):
    session = getSessionLocal()
    voyage = session.query(Voyage).filter(Voyage.code.like("%"+text+"%")).all()
    session.close()
    return voyage

def search_voyage_entre_date(date_debut =None,date_fin=None):
    session = getSessionLocal()

    voyage = session.query(Voyage)
    if date_debut:
        voyage = voyage.filter(Voyage.date_arrive >= date_debut)
    if date_fin :
        voyage = voyage.filter(Voyage.date_arrive <= date_fin)
    voyage = voyage.all()
    session.close()
    return voyage
