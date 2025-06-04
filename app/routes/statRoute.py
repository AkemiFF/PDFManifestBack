from fastapi import APIRouter
from app.services.cargoProduitService import getAllProduit,getNombreCargoAllPays,getNombreVoyageAllVessel

router = APIRouter()


@router.get("/getAllProduit")
def get_all_produit():
    return getAllProduit()

@router.get("/nombre_cargo_pays")
def nombre_all_produit():
    return getNombreCargoAllPays()

@router.get("/nombre_voyage_vessel")
def nombre_all_vessel():
    return getNombreVoyageAllVessel()