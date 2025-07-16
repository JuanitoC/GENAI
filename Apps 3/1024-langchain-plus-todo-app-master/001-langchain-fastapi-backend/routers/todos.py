# todos.py
# Router de FastAPI para exponer los endpoints relacionados con la gestión de tareas (ToDo) y funciones de LangChain

from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
import schemas
import crud
from database import SessionLocal
from langchain import OpenAI, PromptTemplate
from langchain.chains import LLMChain

# Crear el router con el prefijo '/todos'
router = APIRouter(
    prefix="/todos"
)

# Dependencia para obtener una sesión de base de datos por petición
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint para crear una tarea
def create_todo(todo: schemas.ToDoRequest, db: Session = Depends(get_db)):
    todo = crud.create_todo(db, todo)
    return todo

# Endpoint para obtener todas las tareas o filtrar por completadas/no completadas
@router.get("", response_model=List[schemas.ToDoResponse])
def get_todos(completed: bool = None, db: Session = Depends(get_db)):
    todos = crud.read_todos(db, completed)
    return todos

# Endpoint para obtener una tarea por su ID
@router.get("/{id}")
def get_todo_by_id(id: int, db: Session = Depends(get_db)):
    todo = crud.read_todo(db, id)
    if todo is None:
        raise HTTPException(status_code=404, detail="to do not found")
    return todo

# Endpoint para actualizar una tarea por su ID
@router.put("/{id}")
def update_todo(id: int, todo: schemas.ToDoRequest, db: Session = Depends(get_db)):
    todo = crud.update_todo(db, id, todo)
    if todo is None:
        raise HTTPException(status_code=404, detail="to do not found")
    return todo

# Endpoint para eliminar una tarea por su ID
@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_todo(id: int, db: Session = Depends(get_db)):
    res = crud.delete_todo(db, id)
    if res is None:
        raise HTTPException(status_code=404, detail="to do not found")
    
# --- Funcionalidades LangChain ---
# Inicializar el modelo de lenguaje de OpenAI
langchain_llm = OpenAI(temperature=0)

# Plantilla y cadena para resumir texto
summarize_template_string = """
        Provide a summary for the following text:
        {text}
"""

summarize_prompt = PromptTemplate(
    template=summarize_template_string,
    input_variables=['text'],
)

summarize_chain = LLMChain(
    llm=langchain_llm,
    prompt=summarize_prompt,
)

# Endpoint para resumir texto usando LLMChain
@router.post('/summarize-text')
async def summarize_text(text: str):
    summary = summarize_chain.run(text=text)
    return {'summary': summary}

# Plantilla y cadena para generar un poema a partir del texto de una tarea
write_poem_template_string = """
        Write a short poem with the following text:
        {text}
"""

write_poem_prompt = PromptTemplate(
    template=write_poem_template_string,
    input_variables=['text'],
)

write_poem_chain = LLMChain(
    llm=langchain_llm,
    prompt=write_poem_prompt,
)

# Endpoint para generar un poema a partir del nombre de una tarea
@router.post("/write-poem/{id}")
async def write_poem_by_id(id: int, db: Session = Depends(get_db)):
    todo = crud.read_todo(db, id)
    if todo is None:
        raise HTTPException(status_code=404, detail="to do not found")
    poem = write_poem_chain.run(text=todo.name)
    return {'poem': poem}