"""
CRUD (Create, Read, Update, Delete) operations for the ToDo application.

This module contains all database operations for managing ToDo items.
It provides functions to create, read, update, and delete todo items
from the database using SQLAlchemy ORM.
"""

from sqlalchemy.orm import Session
import models, schemas


def create_todo(db: Session, todo: schemas.ToDoRequest) -> models.ToDo:
    """
    Create a new ToDo item in the database.
    
    Args:
        db (Session): SQLAlchemy database session
        todo (schemas.ToDoRequest): ToDo item data containing name and completed status
        
    Returns:
        models.ToDo: The created ToDo item with database-generated ID
        
    Example:
        >>> todo_data = schemas.ToDoRequest(name="Buy groceries", completed=False)
        >>> new_todo = create_todo(db, todo_data)
    """
    # Create a new ToDo model instance with the provided data
    db_todo = models.ToDo(name=todo.name, completed=todo.completed)
    
    # Add the new todo to the database session
    db.add(db_todo)
    
    # Commit the transaction to persist changes
    db.commit()
    
    # Refresh the object to get the database-generated ID
    db.refresh(db_todo)
    
    return db_todo


def read_todos(db: Session, completed: bool | None = None) -> list[models.ToDo]:
    """
    Retrieve ToDo items from the database with optional filtering.
    
    Args:
        db (Session): SQLAlchemy database session
        completed (bool, optional): Filter by completion status. 
                                  If None, returns all todos.
                                  If True, returns only completed todos.
                                  If False, returns only incomplete todos.
        
    Returns:
        list[models.ToDo]: List of ToDo items matching the filter criteria
        
    Example:
        >>> all_todos = read_todos(db)  # Get all todos
        >>> completed_todos = read_todos(db, completed=True)  # Get only completed
        >>> pending_todos = read_todos(db, completed=False)  # Get only pending
    """
    if completed is None:
        # Return all todos when no filter is specified
        return db.query(models.ToDo).all()
    else:
        # Filter todos by completion status
        return db.query(models.ToDo).filter(models.ToDo.completed == completed).all()


def read_todo(db: Session, id: int) -> models.ToDo | None:
    """
    Retrieve a specific ToDo item by its ID.
    
    Args:
        db (Session): SQLAlchemy database session
        id (int): The unique identifier of the ToDo item
        
    Returns:
        models.ToDo | None: The ToDo item if found, None otherwise
        
    Example:
        >>> todo = read_todo(db, 1)
        >>> if todo:
        ...     print(f"Found todo: {todo.name}")
    """
    return db.query(models.ToDo).filter(models.ToDo.id == id).first()


def update_todo(db: Session, id: int, todo: schemas.ToDoRequest) -> models.ToDo | None:
    """
    Update an existing ToDo item in the database.
    
    Args:
        db (Session): SQLAlchemy database session
        id (int): The unique identifier of the ToDo item to update
        todo (schemas.ToDoRequest): New data for the ToDo item
        
    Returns:
        models.ToDo | None: The updated ToDo item if found, None otherwise
        
    Example:
        >>> update_data = schemas.ToDoRequest(name="Updated task", completed=True)
        >>> updated_todo = update_todo(db, 1, update_data)
    """
    # First check if the todo exists
    db_todo = db.query(models.ToDo).filter(models.ToDo.id == id).first()
    
    if db_todo is None:
        # Return None if todo doesn't exist
        return None
    
    # Update the todo with new data
    db.query(models.ToDo).filter(models.ToDo.id == id).update({
        'name': todo.name, 
        'completed': todo.completed
    })
    
    # Commit the transaction
    db.commit()
    
    # Refresh the object to get updated data
    db.refresh(db_todo)
    
    return db_todo


def delete_todo(db: Session, id: int) -> bool:
    """
    Delete a ToDo item from the database.
    
    Args:
        db (Session): SQLAlchemy database session
        id (int): The unique identifier of the ToDo item to delete
        
    Returns:
        bool: True if the todo was successfully deleted, False if not found
        
    Example:
        >>> success = delete_todo(db, 1)
        >>> if success:
        ...     print("Todo deleted successfully")
    """
    # First check if the todo exists
    db_todo = db.query(models.ToDo).filter(models.ToDo.id == id).first()
    
    if db_todo is None:
        # Return False if todo doesn't exist
        return False
    
    # Delete the todo from the database
    db.query(models.ToDo).filter(models.ToDo.id == id).delete()
    
    # Commit the transaction
    db.commit()
    
    return True