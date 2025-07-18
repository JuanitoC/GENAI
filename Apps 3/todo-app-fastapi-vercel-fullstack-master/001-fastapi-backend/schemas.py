# Importación de BaseModel de Pydantic para validación de datos
from pydantic import BaseModel

# Esquema para las solicitudes de creación/actualización de tareas
# Define la estructura de datos que se espera recibir en las peticiones
class ToDoRequest(BaseModel):
    name: str      # Nombre de la tarea (requerido)
    completed: bool # Estado de completado de la tarea (requerido)

# Esquema para las respuestas de tareas
# Define la estructura de datos que se devuelve en las respuestas
class ToDoResponse(BaseModel):
    name: str      # Nombre de la tarea
    completed: bool # Estado de completado de la tarea
    id: int        # ID único de la tarea

    # Configuración del modelo
    class Config:
        orm_mode = True  # Permite que Pydantic trabaje con objetos ORM de SQLAlchemy