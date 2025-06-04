from app.config.database import getSessionLocal
from app.models.model import VinProduit

def createVinProduit(cargo_id,vin):
    session = getSessionLocal()

    newVin = VinProduit(
        cargo_id = cargo_id,
        vin = vin
    )

    session.add(newVin)
    session.commit()
    session.refresh(newVin)
    session.close()
    return newVin

def getVinByCargo(cargo):
    session = getSessionLocal()
    vins = session.query(VinProduit).filter_by(cargo_id= cargo).all()
    session.close()
    return vins