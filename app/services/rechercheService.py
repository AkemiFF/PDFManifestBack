import numpy as np
from app.models.model import Contenu,FilePDF
from app.config.database import getSessionLocal
from app.services.filePDFService import getById

def levenshtein_distance(s1, s2):
    # Crée une matrice de zéros de taille (len(s1) + 1) x (len(s2) + 1)
    matrix = np.zeros((len(s1) + 1, len(s2) + 1))

    # Initialise la première ligne et la première colonne avec les indices
    for i in range(len(s1) + 1):
        matrix[i][0] = i
    for j in range(len(s2) + 1):
        matrix[0][j] = j

    # Remplit la matrice avec les distances de Levenshtein
    for i in range(1, len(s1) + 1):
        for j in range(1, len(s2) + 1):
            if s1[i - 1] == s2[j - 1]:
                cost = 0
            else:
                cost = 1
            matrix[i][j] = min(
                matrix[i - 1][j] + 1,      # Suppression
                matrix[i][j - 1] + 1,      # Insertion
                matrix[i - 1][j - 1] + cost  # Substitution
            )

    # La distance de Levenshtein est la valeur en bas à droite de la matrice
    return matrix[len(s1)][len(s2)]

def sont_presque_pareils(s1, s2, pourcentage=0.1):
    max_length = max(len(s1), len(s2))
    seuil = int(max_length * pourcentage)
    distance = levenshtein_distance(s1, s2)
    return distance <= seuil

def search_in_contenu(text):
    result = []
    session = getSessionLocal()
    contenus = session.query(Contenu).filter(Contenu.contenu.like("%"+text+"%")).all()
    
    for contenu in contenus:
        filePDF = getById(contenu.pdf_id)
        data = {
            "pdf_file_id":contenu.pdf_id,
            "pdf_file" : filePDF.nom,
            "page":contenu.page
        }
        result.append(data)

    session.close()
    return result

def search_pdf_name(text):
    session = getSessionLocal()
    resultat = session.query(FilePDF).filter(FilePDF.nom.like("%"+text+"%")).all()
    session.close()
    return resultat

