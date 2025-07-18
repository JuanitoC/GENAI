# schemas.py
# Esquemas de Pydantic para validar y estructurar datos de entrada y salida relacionados con PDFs

from pydantic import BaseModel
from typing import Optional

# Esquema para solicitudes de creación/actualización de PDF
class PDFRequest(BaseModel):
    name: str  # Nombre del PDF
    selected: bool  # Si el PDF está seleccionado
    file: str  # URL o ruta del archivo PDF

# Esquema para respuestas de PDF (incluye el ID)
class PDFResponse(BaseModel):
    id: int  # ID único del PDF
    name: str  # Nombre del PDF
    selected: bool  # Si el PDF está seleccionado
    file: str  # URL o ruta del archivo PDF

    class Config:
        from_attributes = True  # Permite crear el esquema desde un ORM