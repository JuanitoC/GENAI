# Importaciones necesarias para SQLAlchemy
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# Importación de la clase Base para los modelos
from database import Base


# Modelo de datos para las tareas (ToDo)
# Esta clase define la estructura de la tabla 'todos' en la base de datos
class ToDo(Base):
    # Nombre de la tabla en la base de datos
    __tablename__ = "todos"

    # Campo ID: Clave primaria autoincremental con índice
    id = Column(Integer, primary_key=True, index=True)
    
    # Campo nombre: Texto que describe la tarea
    name = Column(String)
    
    # Campo completado: Booleano que indica si la tarea está completada
    # Por defecto es False (no completada)
    completed = Column(Boolean, default=False)