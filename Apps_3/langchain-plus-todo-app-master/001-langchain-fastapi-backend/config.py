# config.py
# Configuración de variables de entorno para la app FastAPI To Do

from pydantic_settings import BaseSettings

# Clase para gestionar la configuración de la app usando variables de entorno
class Settings(BaseSettings):
    DATABASE_HOST: str  # Host de la base de datos
    DATABASE_NAME: str  # Nombre de la base de datos
    DATABASE_USER: str  # Usuario de la base de datos
    DATABASE_PASSWORD: str  # Contraseña de la base de datos
    DATABASE_PORT: int  # Puerto de la base de datos
    app_name: str = "Full Stack To Do App"  # Nombre de la app

    class Config:
        env_file = ".env"  # Archivo de variables de entorno
        extra = "ignore"  # Ignorar variables extra
