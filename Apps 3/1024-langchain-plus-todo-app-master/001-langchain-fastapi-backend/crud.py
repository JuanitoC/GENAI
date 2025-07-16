# crud.py
# Funciones CRUD para la gestión de tareas (ToDo)

from sqlalchemy.orm import Session
import models, schemas

# Crear una nueva tarea en la base de datos
def create_todo(db: Session, todo: schemas.ToDoRequest):
    db_todo = models.ToDo(name=todo.name, completed=todo.completed)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

# Leer todas las tareas o filtrar por completadas/no completadas
def read_todos(db: Session, completed: bool):
    if completed is None:
        return db.query(models.ToDo).all()
    else:
        return db.query(models.ToDo).filter(models.ToDo.completed == completed).all()

# Leer una tarea por su ID
def read_todo(db: Session, id: int):
    return db.query(models.ToDo).filter(models.ToDo.id == id).first()

# Actualizar una tarea existente por ID
def update_todo(db: Session, id: int, todo: schemas.ToDoRequest):
    db_todo = db.query(models.ToDo).filter(models.ToDo.id == id).first()
    if db_todo is None:
        return None
    db.query(models.ToDo).filter(models.ToDo.id == id).update({'name': todo.name, 'completed': todo.completed})
    db.commit()
    db.refresh(db_todo)
    return db_todo

# Eliminar una tarea por ID
def delete_todo(db: Session, id: int):
    db_todo = db.query(models.ToDo).filter(models.ToDo.id == id).first()
    if db_todo is None:
        return None
    db.query(models.ToDo).filter(models.ToDo.id == id).delete()
    db.commit()
    return True