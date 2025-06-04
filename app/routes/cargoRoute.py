from fastapi import APIRouter,Path
from pydantic import BaseModel
from app.services.cargoService import getAllByManifest,createCargo

router = APIRouter()

@router.get("/getAll/{id}")
def getAllCargoByManifest(id:int):
    result = getAllByManifest(id)
    return result

class AddCargo(BaseModel):
    numero_bl:str
    shipper_id:int
    consigne_id:int
    description:str
    weight:str
    mesurement:str

@router.post("/create/{id}")
def createNewCargo(id:int = Path(...,description="ID du manifest"),request:AddCargo = None):
    createCargo(
        bl_no=request.numero_bl,
        manifest_id= id,
        shipper_id= request.shipper_id,
        consigne_id= request.consigne_id,
        weight= request.weight,
        mesurement= request.mesurement,
        description= request.description
    )
    return {"success":"true"}