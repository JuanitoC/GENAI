# Importaciones necesarias para FastAPI y funcionalidades adicionales
from functools import lru_cache
from typing import Union

from fastapi import FastAPI, Depends
from fastapi.responses import PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.middleware.cors import CORSMiddleware

# Importación del router de todos (comentado hasta que se cree)
from routers import todos

# Importación de la configuración
import config

# Creación de la instancia principal de FastAPI
app = FastAPI()

# Inclusión del router de todos en la aplicación principal
# (comentado hasta que se cree el router)
app.include_router(todos.router)


# Configuración de orígenes permitidos para CORS
#origins = [
#    "http://localhost:3000",
#    "https://todo-frontend-khaki.vercel.app/",
#]

# Configuración de CORS (Cross-Origin Resource Sharing)
# Necesario para permitir que el frontend se comunique con el backend
# En desarrollo, permite todos los orígenes ("*")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todos los orígenes
    allow_credentials=True,  # Permite credenciales (cookies, headers de autorización)
    allow_methods=["*"],  # Permite todos los métodos HTTP
    allow_headers=["*"],  # Permite todos los headers
)


# Manejador global de excepciones HTTP
# Captura todas las excepciones HTTP y las maneja de forma consistente
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    print(f"{repr(exc)}")  # Imprime la excepción para debugging
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)

# Función para obtener la configuración de la aplicación
# Usa lru_cache para cachear la configuración y evitar recargarla
@lru_cache()
def get_settings():
    return config.Settings()


# Endpoint raíz de la aplicación
@app.get("/")
def read_root(settings: config.Settings = Depends(get_settings)):
    # Imprime el nombre de la aplicación desde la configuración
    print(settings.app_name)
    return "Hello World"


# Endpoint de ejemplo para obtener un item por ID
@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}