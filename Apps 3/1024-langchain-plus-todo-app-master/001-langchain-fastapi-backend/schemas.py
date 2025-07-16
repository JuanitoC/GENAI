# schemas.py
# Esquemas de Pydantic para validar y estructurar datos de entrada y salida relacionados con tareas (ToDo)

from pydantic import BaseModel

# Esquema para solicitudes de creación/actualización de tarea
class ToDoRequest(BaseModel):
    name: str  # Nombre o descripción de la tarea
    completed: bool  # Estado de completado

# Esquema para respuestas de tarea (incluye el ID)
class ToDoResponse(BaseModel):
    name: str  # Nombre o descripción de la tarea
    completed: bool  # Estado de completado
    id: int  # ID único de la tarea

    class Config:
        orm_mode = True  # Permite crear el esquema desde un ORM