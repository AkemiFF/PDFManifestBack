from typing import List, Union
from datetime import datetime
from sqlalchemy.orm import Session
from app.config.database import getSessionLocal

from app.models.model import ManifestEntry

def save_manifest_entries(
    data: Union[List[dict], List[List[dict]]]
) -> List[ManifestEntry]:
    """
    Insère en base les objets JSON extraits par l'IA.
    - db: session SQLAlchemy.
    - data: soit une liste de dicts, soit une liste de listes de dicts.
    Retourne la liste des ManifestEntry insérés ou mis à jour.
    """
    db = getSessionLocal()
    flat: List[dict] = []
    for batch in data:
        if isinstance(batch, list):
            flat.extend(batch)
        elif isinstance(batch, dict):
            flat.append(batch)
        else:
            raise ValueError(f"Type inattendu dans data: {type(batch)}")

    entries: List[ManifestEntry] = []
    for item in flat:
        # Conversion du champ DATE en date Python
        date_val = None
        if item.get("DATE"):
            try:
                date_val = datetime.strptime(item["DATE"], "%Y-%m-%d").date()
            except ValueError:
                # tu peux choisir de logger / lever selon le cas
                date_val = None

        # Création ou mise à jour de l'entrée
        entry = ManifestEntry(
            # id             = item["ID"],
            Name           = item["Name"],
            Flag           = item.get("Flag"),
            Produits       = item.get("Produits"),
            Volume         = item.get("Volume"),
            Poids          = item["Poids"],
            Date           = date_val
        )
        # .merge() permet insert ou update si PK déjà existant
        merged = db.merge(entry)
        entries.append(merged)

    db.commit()
    return entries
