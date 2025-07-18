# Importación de BaseSettings de pydantic para manejo de configuración
from pydantic_settings import BaseSettings

# Clase de configuración que hereda de BaseSettings
# Esta clase maneja todas las variables de configuración de la aplicación
class Settings(BaseSettings):
    # Configuración de la base de datos
    DATABASE_HOST: str      # Host de la base de datos
    DATABASE_NAME: str      # Nombre de la base de datos
    DATABASE_USER: str      # Usuario de la base de datos
    DATABASE_PASSWORD: str  # Contraseña de la base de datos
    DATABASE_PORT: int      # Puerto de la base de datos
    
    # Nombre de la aplicación con valor por defecto
    app_name: str = "Full Stack To Do App"

    # Configuración interna de la clase
    class Config:
        env_file = ".env"    # Archivo de variables de entorno a cargar
        extra = "ignore"     # Ignora variables extra no definidas en el modelo
