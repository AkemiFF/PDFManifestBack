from app.services.userService import getAll,createNewUser,updateUser,deleteUser
from fastapi import APIRouter,HTTPException
from pydantic import BaseModel

router = APIRouter()



@router.get("/getAllUser")
def getAllUser() : 
    utilisateurs = getAll()
    return utilisateurs

class AddUserRequest(BaseModel):
    identifiant : str
    password : str

class UserRequest(BaseModel):
    id:int
    identifiant:str
    password:str


@router.post("/create_user")
def createUser(request:AddUserRequest):
    createNewUser(identifiant=request.identifiant,password=request.password)
    return {"success":"true"}


@router.put("/update_user")
def update(request:UserRequest):
    updateUser(id = request.id,identifiant= request.identifiant,password = request.password)
    return {"success":"user"}

@router.delete("/delete/{id}")
def delete(id:int):
    deleteUser(id)
    return {"success":"user"}