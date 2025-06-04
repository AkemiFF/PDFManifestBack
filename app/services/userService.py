import jwt
from app.config.database import getSessionLocal
from app.services.tokenService import create_access_token
from app.models.model import Utilisateur
from datetime import date


SECRET_KEY = "kjdqslkdjsqlkdjsqkdsqjdlkqsjdqlkjdkqlfjqskdfjqk"
ALGORITHM = "HS256"

def login(identifiant,password):    
    session = getSessionLocal()


    utilisateur = session.query(Utilisateur).filter_by(identifiant=identifiant).first()

    if utilisateur is None:
        session.close()
        return {"error":"Utilisateur inconnue"}
     
    if  utilisateur.password == password :
        session.commit()
        data = {"token":create_access_token({"user_id":utilisateur.id,"identifiant":utilisateur.identifiant})}
        session.close()
        return data
    else :
        session.close()
        return {"error":"Mot de passe incorrect"}
    

def verifyToken(token) :
    try :
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return 0
    except jwt.InvalidTokenError:
        return 1
    
def getAll():
    session = getSessionLocal()
    utilisateurs = session.query(Utilisateur).all()
    return {"data":utilisateurs}

def createNewUser(identifiant,password):
    session = getSessionLocal()
    today = date.today()
    newUtilisateur = Utilisateur(identifiant=identifiant,password=password,date_create = today,date_login=today)
    session.add(newUtilisateur)
    session.commit()
    session.refresh(newUtilisateur)
    session.close()
    return newUtilisateur

def updateUser(id,identifiant,password):
    session = getSessionLocal()
    utilisateur = session.query(Utilisateur).filter_by(id = id).first()

    if utilisateur is None :
        return {"error":"null"}
    
    utilisateur.identifiant = identifiant
    utilisateur.password = password

    session.commit()
    session.close()
    return utilisateur

def deleteUser(id) : 
    session = getSessionLocal()
    utilisateur = session.query(Utilisateur).filter_by(id = id).first()

    if utilisateur is None :
        return {"error":"null"}
    
    session.delete(utilisateur)
    session.commit()
    session.close()

