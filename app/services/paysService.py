from app.config.database import getSessionLocal
from app.models.model import PaysOrigine
from app.services.rechercheService import sont_presque_pareils

def getOrCreatePays(pays_name):
    session = getSessionLocal()
    all_pays = session.query(PaysOrigine).all()
    for pays in all_pays : 
        if sont_presque_pareils(pays_name,pays.pays):
            session.close()
            return pays
        
    new_pays = PaysOrigine(
        pays=pays_name
    )

    session.add(new_pays)
    session.commit()
    session.refresh(new_pays)
    session.close()
    return new_pays

def getPaysById(id):
    session = getSessionLocal()
    pays = session.query(PaysOrigine).filter_by(id = id).first()
    session.close()
    return pays

def getAllPays(): 
    session = getSessionLocal()
    pays = session.query(PaysOrigine).all()
    session.close()
    return pays