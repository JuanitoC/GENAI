# main.py
# Archivo principal de la app FastAPI para gestión de tareas (ToDo)

from functools import lru_cache
from typing import Union

from fastapi import FastAPI, Depends
from fastapi.responses import PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.middleware.cors import CORSMiddleware

# Importar el router de tareas
from routers import todos

import config

# Crear la instancia de la aplicación FastAPI
app = FastAPI()

# Incluir el router de tareas para exponer los endpoints relacionados
app.include_router(todos.router)

# Configuración de CORS para permitir peticiones desde cualquier origen (útil para desarrollo frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Manejador global de excepciones HTTP para mostrar errores de forma controlada
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    print(f"{repr(exc)}")
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)

# Función para obtener la configuración de la app usando lru_cache
@lru_cache()
def get_settings():
    return config.Settings()

# Endpoint raíz para comprobar que la app está funcionando
@app.get("/")
def read_root(settings: config.Settings = Depends(get_settings)):
    # Imprime el nombre de la app desde la configuración
    print(settings.app_name)
    return "Hello World"

# Endpoint de ejemplo para obtener un ítem por ID
@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}