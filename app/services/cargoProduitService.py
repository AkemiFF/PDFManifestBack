from app.models.model import CargoProduit
from app.config.database import getSessionLocal
from app.services.cargoService import getAllCargo,getCargoByPays
from app.services.paysService import getPaysById,getAllPays
from app.services.voyageService import getVoyageById,getVoyageByVessel
from app.services.vesselService import getVesselId,getAllVessel

def createCargoProduit(produit , cargo_id, description_produit): 
    session = getSessionLocal()

    newCargoProduit = CargoProduit(
        produit = produit,
        cargo_id = cargo_id,
        description_produit = description_produit
    )

    session.add(newCargoProduit)

    session.commit()
    session.refresh(newCargoProduit)
    session.close()

    return newCargoProduit


def getCargo_ProduitByCargo(cargo_id):
    session = getSessionLocal()
    cargo_produit = session.query(CargoProduit).filter_by(cargo_id = cargo_id).all()
    session.close()
    return cargo_produit


def getAllProduit():
    cargos = getAllCargo()
    all_produit = []
    for cargo in cargos :
        pays_origine = getPaysById(id= cargo.pays_origine_id)   
        produits = getCargo_ProduitByCargo(cargo_id= cargo.id)
        voyage = getVoyageById(id= cargo.voyage_id)
        vessel = getVesselId(id= voyage.vessel_id) 
        for produit in produits:
            data = {
                "produit":produit,
                "pays_origine" : pays_origine,
                "vessel":vessel,
                "voyage":voyage
            }
            all_produit.append(data)

    return all_produit


def getNombreCargoAllPays():
    all_pays = getAllPays()
    datas = []
    for pays in all_pays:
        cargos = getCargoByPays(pays_id= pays.id)
        data = {
            "pays":pays,
            "nombre_cargo": len(cargos)
        }
        datas.append(data)

    return datas

def getNombreVoyageAllVessel():
    vessels = getAllVessel()
    datas = []
    for vessel in vessels :
        voyages = getVoyageByVessel(vessel_id= vessel.id)
        data = {
            "vessel":vessel,
            "nombre_voyage": len(voyages)
        }
        datas.append(data)

    return datas



