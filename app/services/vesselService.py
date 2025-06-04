from app.config.database import getSessionLocal
from app.services.rechercheService import sont_presque_pareils
from app.models.model import Vessel

def getAllVessel():
    session = getSessionLocal()
    vessels = session.query(Vessel).all()
    session.close()
    return vessels

def getVesselByName(name):
    session = getSessionLocal()
    vessel = session.query(Vessel).filter_by(name=name).first()
    session.close()
    return vessel

def getAllVesselByFlag(flag):
    session = getSessionLocal()
    vessels = session.query(Vessel).filter_by(flag = flag).all()
    session.close()
    return vessels

def getVesselId(id):
    session = getSessionLocal()
    vessel = session.query(Vessel).filter_by(id = id).first()
    session.close()
    return vessel

def createNewVessel(name,flag):
    session = getSessionLocal()
    newVessel = Vessel(name = name,flag = flag)
    session.add(newVessel)
    session.commit()
    session.refresh(newVessel)
    session.close()
    return newVessel

def updateVessel(id,name,flag):
    vessel = getVesselId(id)
    if vessel is None : 
        raise Exception("Erreur update")
    
    vessel.name = name
    vessel.flag = flag

    session = getSessionLocal()
    session.commit()
    session.close()
    return vessel

def deleteVessel(id):
    vessel = getVesselId(id)
    if vessel is None : 
        raise Exception("Erreur update")
    
    session = getSessionLocal()
    session.delete(vessel)
    session.commit()
    session.close()
    

def createOrGetVessel(name,flag):
    vessel = getVesselByName(name)
    if not vessel :
        vessel = createNewVessel(
            name= name,
            flag= flag
        )
    return vessel


def searchVesselByName(text):
    session = getSessionLocal()
    resultat = session.query(Vessel).filter(Vessel.name.like("%"+text+"%")).all() 
    session.close()
    return resultat

def getAllFlag():
    session = getSessionLocal()
    vessels = session.query(Vessel).all()
    session.close()
    flags = []
    for vessel in vessels :
        flags.append(vessel.flag)
    
    return flags