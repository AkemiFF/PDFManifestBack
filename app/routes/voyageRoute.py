from fastapi import APIRouter,HTTPException
from pydantic import BaseModel
from app.services.voyageService import getAllVoyage,getVoyageByVessel,createNewVoyage
from datetime import datetime

router= APIRouter()


@router.get("/getAll")
def getAll():
    resultats = getAllVoyage()
    return resultats

@router.get("/get/{id}")
def getByVessel(id:int):
    resultats = getVoyageByVessel(id)
    return resultats

class AddVoyage(BaseModel):
    code:str
    date_arrive:str
    
@router.post("/add/{id}")
def addNewVoyage(id:int ,request:AddVoyage):
    date_arrive = datetime.strptime(request.date_arrive,"%Y-%m-%d")
    resultat = createNewVoyage(
        code= request.code,
        date_arrive=date_arrive,
        vessel_id= id
    )
    return resultat