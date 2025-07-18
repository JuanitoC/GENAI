"""
Migración para crear la tabla todos

Revision ID: ad1c380734f8
Revises: 
Create Date: 2023-12-03 13:25:00.622096

Esta migración crea la tabla 'todos' en la base de datos PostgreSQL
con los campos necesarios para la aplicación de tareas.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# Identificadores de revisión, utilizados por Alembic
revision: str = 'ad1c380734f8'  # ID único de esta migración
down_revision: Union[str, None] = None  # Migración anterior (None si es la primera)
branch_labels: Union[str, Sequence[str], None] = None  # Etiquetas de rama
depends_on: Union[str, Sequence[str], None] = None  # Dependencias de otras migraciones


def upgrade():
    """
    Función de actualización: Crea la tabla todos
    
    Esta función se ejecuta cuando se aplica la migración hacia adelante.
    Crea la tabla 'todos' con los siguientes campos:
    - id: Clave primaria autoincremental (bigserial)
    - name: Campo de texto para el nombre de la tarea
    - completed: Campo booleano para el estado de completado (por defecto false)
    """
    op.execute("""
    create table todos(
        id bigserial primary key,  -- ID autoincremental como clave primaria
        name text,                 -- Nombre de la tarea
        completed boolean not null default false  -- Estado completado (por defecto false)
    )
    """)

def downgrade():
    """
    Función de reversión: Elimina la tabla todos
    
    Esta función se ejecuta cuando se revierte la migración.
    Elimina completamente la tabla 'todos' de la base de datos.
    """
    op.execute("drop table todos;")
