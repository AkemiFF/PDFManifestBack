from app.config.database import getSessionLocal
from app.models.model import Cargo
from decimal import Decimal
from app.services.rechercheService import sont_presque_pareils
from datetime import datetime
from app.services.paysService import getOrCreatePays

def getAllCargo():
    session = getSessionLocal()
    cargos = session.query(Cargo).filter_by().all()
    session.close()
    return cargos 
    

def createCargo(voyage_id,port_depart,shipper,consigne,bl_no,poid,volume,pays_name,quantite):
    session = getSessionLocal()
    
    pays_origine = getOrCreatePays(pays_name=pays_name)
    
    newCargo = Cargo(
        voyage_id = voyage_id,
        bl_no = bl_no,
        port_depart = port_depart,
        shipper = shipper,
        consignee = consigne,
        pays_origine_id = pays_origine.id,
        quantite = int(quantite),
        poid = Decimal(poid),
        volume = Decimal(volume)
    )

    session.add(newCargo)
    session.commit()
    session.refresh(newCargo)
    session.close()
    return newCargo

def getCargoByBL(bl_no):
    session = getSessionLocal()
    cargo = session.query(Cargo).filter_by(bl_no = bl_no).first()
    session.close()
    return cargo

def getCargoByVoyage(voyage_id):
    session = getSessionLocal()
    cargo = session.query(Cargo).filter_by(voyage_id = voyage_id).all()
    session.close()
    return cargo


def getCargoByPays(pays_id):
    session = getSessionLocal()
    cargo = session.query(Cargo).filter_by(pays_origine_id = pays_id).all()
    session.close()
    return cargo