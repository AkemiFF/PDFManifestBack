import io
import json
import os
import tempfile
from typing import Generator, List, Optional, Union

import openai
from openai import APIError, AuthenticationError, OpenAI, RateLimitError
from PyPDF2 import PdfReader

from app.models.model import FilePDF
from app.services.pdfToAiService import *


def _format_table(table: List[List[str]]) -> str:
    """
    Convert a list of rows (first row headers) into a markdown-like table string.
    """
    if not table:
        return ""
    try:
        headers = table[0]
        rows = table[1:]
        # build markdown table
        md = "| " + " | ".join(headers) + " |\n"
        md += "| " + " | ".join(['---'] * len(headers)) + " |\n"
        for row in rows:
            md += "| " + " | ".join(row) + " |\n"
        return md
    except Exception:
        # In case of error, return a plain text version of the table
        return "\n".join(["\t".join(str(cell) if cell is not None else "" for cell in row) for row in table])

class AIManager:
    """
    Service class to analyze PDF pages via OpenAI GPT-3.5 with batching,
    offrant le choix d'envoyer le PDF ou le texte formaté.
    """

    def __init__(self, model: str = "gpt-3.5-turbo"):
        import os

        from openai import OpenAI
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = model

    def analyze_pdf_pages(
        self,
        pdf_manager: PDFManager,
        pdf_record: FilePDF,
        start_page: Optional[int] = None,
        end_page: Optional[int] = None,
        batch_size: int = 3,
        mode: str = 'text'
    ) -> List[Union[dict, List[dict]]]:
        """
        Analyse un intervalle de pages, en découpant en lots de batch_size.
        mode='text' (texte formaté) ou 'pdf' (fichier PDF).
        """
        # Détermination de la plage
        path = pdf_manager.get_file_path(pdf_record)
        reader = PdfReader(path)
        total = len(reader.pages)
        sp = start_page or 1
        ep = end_page or total
        if sp < 1 or ep > total or sp > ep:
            raise ValueError(f"Invalid page range: {sp} to {ep} (total {total})")
        pages = list(range(sp, ep + 1))

        # Générer les batches
        batches = [pages[i:i + batch_size] for i in range(0, len(pages), batch_size)]
        results = []
        for batch in batches:
            results.append(self._process_batch(batch, pdf_manager, pdf_record, mode))
        return results

    def _process_batch(
        self,
        pages: List[int],
        pdf_manager: PDFManager,
        pdf_record: FilePDF,
        mode: str
    ) -> Union[dict, List[dict]]:
        """
        Traite un seul lot de pages selon le mode.
        """
        print(pages)
        path = pdf_manager.get_file_path(pdf_record)
        if mode == 'pdf':
            # Construction du PDF réduit
            writer = PdfWriter()
            src = PdfReader(path)
            for num in pages:
                writer.add_page(src.pages[num - 1])
            buffer = io.BytesIO()
            writer.write(buffer)
            buffer.seek(0)
            return self.parse_pdf_file(buffer.read())
        # mode 'text'
        segments = []
        for num in pages:
            struct = pdf_manager.extract_structured(pdf_record, num)
            text = pdf_manager.extract_page_text(pdf_record, num)
            seg = f"--- Page {num} ---{text or ''}"
            for tbl in struct.get("tables", []):
                md = _format_table(tbl)
                if md:
                    seg += f"Tableau:{md}"
            segments.append(seg)
        full_content = "".join(segments)
        return self.parse_text(full_content)

    def parse_text(self, text: str) -> Union[dict, List[dict]]:
        """
        Envoie un prompt contenant du texte à l'API et parse la réponse JSON.
        """
      
        prompt = (
            "Lis le contenu suivant (texte et tableaux) et retourne en JSON un ou plusieurs objets "
            "avec les champs : Name (texte, vessel (nom du navire)), Flag (code pays), "
            "Volume (nombre, m3), Poids (nombre, kg), DATE (date). "
            "Si plusieurs éléments sont détectés, renvoie une liste JSON. "
            "Contenu :" + text
        )
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": "Génère UNIQUEMENT le JSON valide."}
        ]
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0
            )
            full_response = response.choices[0].message.content.strip()
            return json.loads(full_response)
        except (APIError, RateLimitError, AuthenticationError) as e:
            return {"error": str(e)}
        except json.JSONDecodeError:
            return {"error": "Invalid response format", "raw": full_response}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}

    def parse_pdf_file(self, pdf_bytes: bytes) -> Union[dict, List[dict]]:
        """
        Envoie un fichier PDF binaire à l'API pour extraction directe.
        """     
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmpf:
            tmpf.write(pdf_bytes)
            tmp_path = tmpf.name
        try:
            # Uploader le fichier pour usage answers
            with open(tmp_path, "rb") as f:
                file_resp = self.client.files.create(
                    file=f,
                    purpose="user_data"
                )
            file_id = file_resp.id
            prompt = (
                "Lis le contenu du fichier et retourne en JSON un ou plusieurs objets "
                "avec les champs : Name (texte, vessel /nom du navire / null), Flag (code pays), Produits (texte, liste des produits séparé avec ',') "
                "Volume (nombre, m3), Poids (nombre, kg), DATE (date). "
                "Si plusieurs éléments sont détectés, renvoie une liste JSON. "               
                "avec tout les cargaisons présent dans le fichier. uniquement en format JSON correcte et rien d'autre (pas de commentaire)."               
            )
            answer = self.client.responses.create(
                model="gpt-4.1",
                input=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "input_file",
                                "file_id": file_id,
                            },
                            {
                                "type": "input_text",
                                "text": prompt,
                            },
                        ]
                    }
                ],                
                temperature=0
            )
            raw = answer.output_text
            # Supprimer d'éventuelles balises Markdown ```json
            clean = raw.strip()
            if clean.startswith("```") and clean.endswith("```"):
                clean = clean.lstrip("```json").rstrip("```").strip()
            print(clean)
            return json.loads(clean)
        except (APIError, RateLimitError, AuthenticationError) as e:
            return {"error": str(e)}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}
        finally:
            try:
                os.remove(tmp_path)
            except:
                pass
