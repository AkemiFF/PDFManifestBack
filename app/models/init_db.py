# init_db.py
from model import \
    Base  # importe ici ton declarative_base() avec ManifestEntry et FilePDF
from sqlalchemy import create_engine

# Exemple de connexion PostgreSQL :
# Remplace user, password, host, port, dbname par tes infos
DATABASE_URL = "postgresql://akemi:akemi@localhost:5432/gestionpdf"

engine = create_engine(DATABASE_URL)

Base.metadata.drop_all(bind=engine) 
Base.metadata.create_all(bind=engine)

print("✅ Tables créées (si elles n'existaient pas déjà).")
