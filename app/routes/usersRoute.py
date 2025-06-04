import pdfplumber
from app.services.userService import login,verifyToken
from pydantic import BaseModel
from fastapi import APIRouter, UploadFile, File,HTTPException,Header

router = APIRouter()


class LoginRequest(BaseModel):
    identifiant:str
    password:str



@router.get("/")
def verify_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code= 401,detail="Token manquante")

    token = authorization.split(" ")[1]
    verification = verifyToken(token)
    if verification == 1 or verification == 0:
        raise HTTPException(status_code= 401,detail="Token manquante")

    return verification


@router.post("/login")
def login_user(request:LoginRequest):
    result = login(request.identifiant,request.password)
    if "error" in result :
        raise HTTPException(status_code= 401,detail=result["error"])

    return result

