from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.middleware.auth_middleware import JWTAuthMiddleware
from app.routes import (adminRoute, pdfRoute, pdfTest, rechercheRoute, statRoute,
                        usersRoute, vesselRoute, voyageRoute)

app = FastAPI()


    # "https://gestion-pdf-front-git-main-mamitiana2004s-projects.vercel.app"

origins = [
    "http://localhost:3000"
]

@app.get("/")
def read_root():
    return {"message": "ATO"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(JWTAuthMiddleware)   


app.include_router(pdfRoute.router, prefix="/api/pdf",tags=["PDFs"])
app.include_router(pdfTest.router, prefix="/test",tags=["test"])
app.include_router(vesselRoute.router,prefix="/vessel",tags=["vessels"])
app.include_router(voyageRoute.router,prefix="/voyage",tags=["voyages"])
app.include_router(usersRoute.router, prefix="/users", tags=["Users"])
app.include_router(adminRoute.router,prefix="/api/admin",tags=["ADMIN"])
app.include_router(rechercheRoute.router,prefix="/api/search",tags=["recherches"])
app.include_router(statRoute.router,prefix="/api/stat",tags=["statistiques"])