from fastapi import APIRouter,HTTPException
from pydantic import BaseModel
from app.services.vesselService import getAllVessel,createNewVessel,updateVessel

router = APIRouter()


@router.get("/getAll")
def getAll():
    resultat = getAllVessel()
    return resultat

class AddVessel(BaseModel):
    name:str
    flag:str

@router.post("/create")
def create(request:AddVessel):
    resultat = createNewVessel(name=request.name,flag=request.flag)
    return resultat

class VesselBaseModel(BaseModel):
    id:int
    name:str
    flag:str

@router.put("/update")
def update(request:VesselBaseModel):
    resultat = updateVessel(id= request.id,name= request.name, flag= request.flag)
    return resultat

