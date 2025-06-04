from typing import List, Tuple

import pdfplumber
from fastapi import File, UploadFile


# Fonction pour extraire le texte d'un PDF page par page
def extract_text_with_plumber(file: UploadFile = File(...)) -> List[Tuple[int, str]]:
    text_data = []
    with pdfplumber.open(file.file) as pdf:
        test = get_number_page(file)
        print(test)
        for page_number,page in enumerate(pdf.pages,start=1):
            text = page.extract_text()
            if verify_reverse(text):
                text= text[::-1]

            if text:
                text_data.append((page_number,text.replace("\n", " ")))

    return text_data

def get_number_page(file:UploadFile = File(...)):
    pdf = pdfplumber.open(file.file)
    return len(pdf.pages)


def verify_reverse(text:str):
    is_reverse = text.__contains__("lesse")
    return is_reverse


