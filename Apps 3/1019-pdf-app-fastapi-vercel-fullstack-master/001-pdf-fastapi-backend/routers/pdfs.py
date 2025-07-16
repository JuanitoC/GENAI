# pdfs.py
# Router de FastAPI para exponer los endpoints relacionados con la gestión de PDFs

from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
import schemas
import crud
from database import SessionLocal
from uuid import uuid4

# Crear el router con el prefijo '/pdfs'
router = APIRouter(prefix="/pdfs")

# Dependencia para obtener una sesión de base de datos por petición
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint para crear un PDF a partir de datos JSON
@router.post("", response_model=schemas.PDFResponse, status_code=status.HTTP_201_CREATED)
def create_pdf(pdf: schemas.PDFRequest, db: Session = Depends(get_db)):
    return crud.create_pdf(db, pdf)

# Endpoint para subir un archivo PDF y almacenarlo en S3
@router.post("/upload", response_model=schemas.PDFResponse, status_code=status.HTTP_201_CREATED)
def upload_pdf(file: UploadFile = File(...), db: Session = Depends(get_db)):
    file_name = f"{uuid4()}-{file.filename}"
    return crud.upload_pdf(db, file, file_name)

# Endpoint para obtener la lista de PDFs, opcionalmente filtrando por 'selected'
@router.get("", response_model=List[schemas.PDFResponse])
def get_pdfs(selected: Optional[bool] = None, db: Session = Depends(get_db)):
    return crud.read_pdfs(db, selected)

# Endpoint para obtener un PDF por su ID
@router.get("/{id}", response_model=schemas.PDFResponse)
def get_pdf_by_id(id: int, db: Session = Depends(get_db)):
    pdf = crud.read_pdf(db, id)
    if pdf is None:
        raise HTTPException(status_code=404, detail="PDF not found")
    return pdf

# Endpoint para actualizar un PDF por su ID
@router.put("/{id}", response_model=schemas.PDFResponse)
def update_pdf(id: int, pdf: schemas.PDFRequest, db: Session = Depends(get_db)):
    updated_pdf = crud.update_pdf(db, id, pdf)
    if updated_pdf is None:
        raise HTTPException(status_code=404, detail="PDF not found")
    return updated_pdf

# Endpoint para eliminar un PDF por su ID
@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_pdf(id: int, db: Session = Depends(get_db)):
    if not crud.delete_pdf(db, id):
        raise HTTPException(status_code=404, detail="PDF not found")
    return {"message": "PDF successfully deleted"}

