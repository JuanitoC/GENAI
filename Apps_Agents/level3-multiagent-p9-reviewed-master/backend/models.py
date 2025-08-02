"""
RESUMEN DEL ARCHIVO:
Este archivo define los modelos de datos Pydantic utilizados en el sistema de investigación multiagente.
Define las estructuras de datos para representar información de áreas de negocio, URLs de artículos de blog
y videos de YouTube. Los modelos incluyen:

- NamedUrl: Para representar URLs con nombres/títulos
- BusinessareaInfo: Para información específica de un área de negocio en una tecnología
- BusinessareaInfoList: Para una lista completa de información de áreas de negocio

Estos modelos se utilizan para estructurar y validar los datos que fluyen entre los agentes
y las tareas del sistema de investigación.
"""

from typing import List
from pydantic import BaseModel


class NamedUrl(BaseModel):
    """
    Modelo para representar una URL con un nombre o título asociado.
    
    Atributos:
        name (str): El nombre o título de la URL
        url (str): La URL completa
    """
    name: str
    url: str


class BusinessareaInfo(BaseModel):
    """
    Modelo para representar información de investigación de un área de negocio específica
    dentro de una tecnología particular.
    
    Atributos:
        technology (str): El nombre de la tecnología (ej: "AI", "Blockchain")
        businessarea (str): El área de negocio específica (ej: "Healthcare", "Finance")
        blog_articles_urls (List[str]): Lista de URLs de artículos de blog encontrados
        youtube_videos_urls (List[NamedUrl]): Lista de videos de YouTube con título y URL
    """
    technology: str
    businessarea: str
    blog_articles_urls: List[str]
    youtube_videos_urls: List[NamedUrl]


class BusinessareaInfoList(BaseModel):
    """
    Modelo contenedor para una lista completa de información de áreas de negocio.
    Representa el resultado final de la investigación multiagente.
    
    Atributos:
        businessareas (List[BusinessareaInfo]): Lista de información de todas las áreas
                                             de negocio investigadas
    """
    businessareas: List[BusinessareaInfo]