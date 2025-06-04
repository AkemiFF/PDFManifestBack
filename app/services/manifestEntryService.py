from datetime import datetime
from typing import List, Union

from app.config.database import getSessionLocal
from app.models.model import ManifestEntry
from sqlalchemy import func
from sqlalchemy.orm import Session


def get_all_manifest_entries() -> List[ManifestEntry]:
    """
    Récupère toutes les entrées de la table manifest_entry.
    Retourne une liste d'instances ManifestEntry.
    """
    db = getSessionLocal()
    try:
        entries: List[ManifestEntry] = db.query(ManifestEntry).all()
        return entries
    finally:
        db.close()
from app.models.model import FilePDF, ManifestEntry


def save_manifest_entries(
    data: Union[List[dict], List[List[dict]]],
    record: FilePDF
) -> List[ManifestEntry]:
    """
    Insère en base les objets JSON extraits par l'IA.
    - data: soit une liste de dicts, soit une liste de listes de dicts.
    Retourne la liste des ManifestEntry insérés ou mis à jour.
    """
    db: Session = getSessionLocal()
    flat: List[dict] = []
    
    # Aplatir la structure (liste de dicts ou liste de listes)
    for batch in data:
        if isinstance(batch, list):
            flat.extend(batch)
        elif isinstance(batch, dict):
            flat.append(batch)
        else:
            raise ValueError(f"Type inattendu dans data: {type(batch)}")

    db.add(record)
    db.flush() 
    last_id = db.query(func.max(ManifestEntry.id)).scalar() or 0
    print(record)
    entries: List[ManifestEntry] = []
    for i, item in enumerate(flat):
        # Conversion du champ "DATE" en date Python, s'il existe
        date_val = None
        if item.get("DATE"):
            try:
                date_val = datetime.strptime(item["DATE"], "%Y-%m-%d").date()
            except ValueError:
                date_val = None

        # Générer un nouvel ID si non fourni dans le JSON
        entry_id = item.get("ID") if "ID" in item else last_id + i + 1

        # Créer l'instance en se basant sur les attributs du modèle (en minuscules)
        entry = ManifestEntry(
            id       = entry_id,
            name     = item.get("Name"),
            flag     = item.get("Flag"),
            produits = item.get("Produits"),
            volume   = item.get("Volume"),
            poids    = item.get("Poids"),
            date     = date_val,
            file_pdf_id = record.id,       # lier au FilePDF inséré
            page        = 1
        )

        # merge() permet d'INSERT ou UPDATE selon que l'ID existe ou non
        merged = db.merge(entry)
        # pour récupérer les champs calculés/auto‐générés si besoin
        db.flush()
        entries.append(merged)

    # On commite après avoir ajouté / mis à jour tous les objets
    db.commit()

    # Après un commit, SQLAlchemy expire par défaut les instances.
    # On les "refresh" pour s'assurer qu'elles sont à jour en session
    for ent in entries:
        db.refresh(ent)

    return entries
