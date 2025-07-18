# models.py
# Definición del modelo ORM para la tabla de tareas (ToDo)

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base

# Modelo ToDo que representa la tabla 'todos' en la base de datos
class ToDo(Base):
    __tablename__ = "todos"  # Nombre de la tabla en la base de datos

    id = Column(Integer, primary_key=True, index=True)  # ID único de la tarea
    name = Column(String)  # Nombre o descripción de la tarea
    completed = Column(Boolean, default=False)  # Estado de completado