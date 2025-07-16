# models.py
# Definición del modelo ORM para la tabla de PDFs

from sqlalchemy import Boolean, Column, LargeBinary, Integer, Text
from database import Base

# Modelo PDF que representa la tabla 'pdfs' en la base de datos
class PDF(Base):
    __tablename__ = "pdfs"  # Nombre de la tabla en la base de datos

    id = Column(Integer, primary_key=True, index=True)  # ID único del PDF
    name = Column(Text)  # Nombre del archivo PDF
    file = Column(Text)  # URL o ruta del archivo PDF
    selected = Column(Boolean, default=False)  # Indica si el PDF está seleccionado