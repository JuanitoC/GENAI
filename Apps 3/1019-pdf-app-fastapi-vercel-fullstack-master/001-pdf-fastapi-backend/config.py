# config.py
# Configuración de variables de entorno y cliente AWS S3 para la app FastAPI

import os
import boto3
from pydantic_settings import BaseSettings

# Clase para gestionar la configuración de la app usando variables de entorno
class Settings(BaseSettings):
    DATABASE_HOST: str  # Host de la base de datos
    DATABASE_NAME: str  # Nombre de la base de datos
    DATABASE_USER: str  # Usuario de la base de datos
    DATABASE_PASSWORD: str  # Contraseña de la base de datos
    DATABASE_PORT: int  # Puerto de la base de datos
    app_name: str = "Full Stack PDF CRUD App"  # Nombre de la app
    AWS_KEY: str  # Clave de AWS
    AWS_SECRET: str  # Secreto de AWS
    AWS_S3_BUCKET: str = "pdf-basic-app"  # Nombre del bucket S3

    # Método estático para obtener un cliente S3 autenticado
    @staticmethod
    def get_s3_client():
        return boto3.client(
            's3',
            aws_access_key_id=Settings().AWS_KEY,
            aws_secret_access_key=Settings().AWS_SECRET
        )

    class Config:
        env_file = ".env"  # Archivo de variables de entorno
        extra = "ignore"  # Ignorar variables extra
