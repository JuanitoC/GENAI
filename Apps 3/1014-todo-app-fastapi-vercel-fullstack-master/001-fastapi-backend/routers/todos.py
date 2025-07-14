# Importaciones necesarias para el router de todos
from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
import schemas
import crud
from database import SessionLocal

# Creación del router con prefijo "/todos"
# Todas las rutas de este router tendrán el prefijo /todos
# Ejemplo: @router.get("") se convierte en GET /todos
router = APIRouter(
    prefix="/todos"
)

# Función de dependencia para obtener la sesión de base de datos
# FastAPI ejecuta esta función antes de cada endpoint y cierra la sesión después
# Esto garantiza que cada request tenga su propia sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db  # Proporciona la sesión al endpoint
    finally:
        db.close()  # Cierra la sesión después de usarla (importante para evitar memory leaks)

# ============================================================================
# ENDPOINT: POST /todos
# ============================================================================
@router.post("", status_code=status.HTTP_201_CREATED)
def create_todo(todo: schemas.ToDoRequest, db: Session = Depends(get_db)):
    """
    Crea una nueva tarea en la base de datos.
    
    FLUJO:
    1. Frontend envía POST /todos con JSON: {"name": "Comprar leche", "completed": false}
    2. FastAPI valida automáticamente el JSON contra schemas.ToDoRequest
    3. Se ejecuta get_db() para obtener sesión de base de datos
    4. Se llama crud.create_todo() que:
       - Crea instancia del modelo ToDo
       - La agrega a la sesión
       - Hace commit a la base de datos
       - Refresca el objeto para obtener el ID generado
    5. Se devuelve la tarea creada con su ID
    
    Args:
        todo: Datos validados por Pydantic (nombre y estado completado)
        db: Sesión de SQLAlchemy (inyectada automáticamente por FastAPI)
    
    Returns:
        models.ToDo: La tarea creada con ID generado por PostgreSQL
        
    Status Codes:
        - 201: Tarea creada exitosamente
        - 422: Datos de entrada inválidos (validado por Pydantic)
    """
    todo = crud.create_todo(db, todo)
    return todo

# ============================================================================
# ENDPOINT: GET /todos
# ============================================================================
@router.get("", response_model=List[schemas.ToDoResponse])
def get_todos(completed: bool = None, db: Session = Depends(get_db)):
    """
    Obtiene todas las tareas, con filtro opcional por estado de completado.
    
    FLUJO:
    1. Frontend envía GET /todos o GET /todos?completed=true
    2. FastAPI extrae el parámetro 'completed' de la query string
    3. Se ejecuta get_db() para obtener sesión de base de datos
    4. Se llama crud.read_todos() que:
       - Si completed=None: SELECT * FROM todos
       - Si completed=True: SELECT * FROM todos WHERE completed = true
       - Si completed=False: SELECT * FROM todos WHERE completed = false
    5. Se devuelve lista de tareas (validada por response_model)
    
    Args:
        completed: Filtro opcional de query parameter
                  - None: Obtiene todas las tareas
                  - True: Solo tareas completadas
                  - False: Solo tareas pendientes
        db: Sesión de SQLAlchemy (inyectada automáticamente)
    
    Returns:
        List[schemas.ToDoResponse]: Lista de tareas que coinciden con el filtro
        
    Status Codes:
        - 200: Lista de tareas obtenida exitosamente
        
    Ejemplos de uso:
        GET /todos → Todas las tareas
        GET /todos?completed=true → Solo completadas
        GET /todos?completed=false → Solo pendientes
    """
    todos = crud.read_todos(db, completed)
    return todos

# ============================================================================
# ENDPOINT: GET /todos/{id}
# ============================================================================
@router.get("/{id}")
def get_todo_by_id(id: int, db: Session = Depends(get_db)):
    """
    Obtiene una tarea específica por su ID.
    
    FLUJO:
    1. Frontend envía GET /todos/123
    2. FastAPI extrae el parámetro 'id' del path
    3. Se ejecuta get_db() para obtener sesión de base de datos
    4. Se llama crud.read_todo() que ejecuta: SELECT * FROM todos WHERE id = 123
    5. Si se encuentra: se devuelve la tarea
    6. Si no se encuentra: se lanza HTTPException(404)
    
    Args:
        id: ID único de la tarea (extraído del path parameter)
        db: Sesión de SQLAlchemy (inyectada automáticamente)
    
    Returns:
        models.ToDo: La tarea si existe
        
    Status Codes:
        - 200: Tarea encontrada y devuelta
        - 404: Tarea no encontrada
        
    Ejemplo de uso:
        GET /todos/123 → Obtiene la tarea con ID 123
    """
    todo = crud.read_todo(db, id)
    if todo is None:
        raise HTTPException(status_code=404, detail="to do not found")
    return todo

# ============================================================================
# ENDPOINT: PUT /todos/{id}
# ============================================================================
@router.put("/{id}")
def update_todo(id: int, todo: schemas.ToDoRequest, db: Session = Depends(get_db)):
    """
    Actualiza una tarea existente por su ID.
    
    FLUJO:
    1. Frontend envía PUT /todos/123 con JSON: {"name": "Nuevo nombre", "completed": true}
    2. FastAPI valida automáticamente el JSON contra schemas.ToDoRequest
    3. Se ejecuta get_db() para obtener sesión de base de datos
    4. Se llama crud.update_todo() que:
       - Verifica si la tarea existe: SELECT * FROM todos WHERE id = 123
       - Si no existe: retorna None
       - Si existe: UPDATE todos SET name = 'Nuevo nombre', completed = true WHERE id = 123
       - Hace commit y refresca el objeto
    5. Si se actualizó: se devuelve la tarea actualizada
    6. Si no se encontró: se lanza HTTPException(404)
    
    Args:
        id: ID único de la tarea a actualizar (extraído del path parameter)
        todo: Nuevos datos validados por Pydantic
        db: Sesión de SQLAlchemy (inyectada automáticamente)
    
    Returns:
        models.ToDo: La tarea actualizada
        
    Status Codes:
        - 200: Tarea actualizada exitosamente
        - 404: Tarea no encontrada
        - 422: Datos de entrada inválidos (validado por Pydantic)
        
    Ejemplo de uso:
        PUT /todos/123 {"name": "Comprar pan", "completed": true}
    """
    todo = crud.update_todo(db, id, todo)
    if todo is None:
        raise HTTPException(status_code=404, detail="to do not found")
    return todo

# ============================================================================
# ENDPOINT: DELETE /todos/{id}
# ============================================================================
@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_todo(id: int, db: Session = Depends(get_db)):
    """
    Elimina una tarea por su ID.
    
    FLUJO:
    1. Frontend envía DELETE /todos/123
    2. FastAPI extrae el parámetro 'id' del path
    3. Se ejecuta get_db() para obtener sesión de base de datos
    4. Se llama crud.delete_todo() que:
       - Verifica si la tarea existe: SELECT * FROM todos WHERE id = 123
       - Si no existe: retorna False
       - Si existe: DELETE FROM todos WHERE id = 123
       - Hace commit
    5. Si se eliminó: se devuelve respuesta exitosa
    6. Si no se encontró: se lanza HTTPException(404)
    
    Args:
        id: ID único de la tarea a eliminar (extraído del path parameter)
        db: Sesión de SQLAlchemy (inyectada automáticamente)
    
    Returns:
        dict: Respuesta de confirmación de eliminación
        
    Status Codes:
        - 200: Tarea eliminada exitosamente
        - 404: Tarea no encontrada
        
    Ejemplo de uso:
        DELETE /todos/123 → Elimina la tarea con ID 123
    """
    res = crud.delete_todo(db, id)
    if res is None:
        raise HTTPException(status_code=404, detail="to do not found")