"""
RESUMEN DEL ARCHIVO:
Este archivo implementa una herramienta personalizada para buscar videos de YouTube
utilizando la API oficial de YouTube. La herramienta está diseñada para ser utilizada
por los agentes de CrewAI para encontrar videos relevantes sobre tecnologías específicas
en diferentes áreas de negocio.

Características principales:
- Integración con la API de YouTube v3
- Búsqueda por palabras clave
- Configuración de número máximo de resultados
- Estructura de datos tipada con Pydantic
- Manejo de errores de API

Requisitos:
- Variable de entorno YOUTUBE_API_KEY configurada
- Conexión a internet para acceder a la API de YouTube
"""

from typing import List, Type
from pydantic.v1 import BaseModel, Field
import os
import requests
from crewai_tools import BaseTool


class VideoSearchResult(BaseModel):
    """
    Modelo para representar el resultado de una búsqueda de video en YouTube.
    
    Atributos:
        title (str): Título del video encontrado
        video_url (str): URL completa del video de YouTube
    """
    title: str
    video_url: str


class YoutubeVideoSearchToolInput(BaseModel):
    """
    Modelo de entrada para la herramienta de búsqueda de YouTube.
    Define los parámetros requeridos para realizar una búsqueda.
    
    Atributos:
        keyword (str): Palabra clave para buscar en YouTube
        max_results (int): Número máximo de resultados a retornar (default: 10)
    """
    keyword: str = Field(..., description="The search keyword.")
    max_results: int = Field(
        10, description="The maximum number of results to return.")


class YoutubeVideoSearchTool(BaseTool):
    """
    Herramienta personalizada de CrewAI para buscar videos en YouTube.
    
    Esta herramienta permite a los agentes buscar videos de YouTube basándose
    en palabras clave específicas, útil para encontrar contenido relevante sobre
    tecnologías en diferentes áreas de negocio.
    
    Atributos:
        name (str): Nombre de la herramienta
        description (str): Descripción de la funcionalidad
        args_schema (Type[BaseModel]): Esquema de argumentos de entrada
    """
    name: str = "Search YouTube Videos"
    description: str = "Searches YouTube videos based on a keyword and returns a list of video search results."
    args_schema: Type[BaseModel] = YoutubeVideoSearchToolInput

    def _run(self, keyword: str, max_results: int = 10) -> List[VideoSearchResult]:
        """
        Ejecuta la búsqueda de videos en YouTube.
        
        Args:
            keyword (str): Palabra clave para buscar
            max_results (int): Número máximo de resultados a retornar
            
        Returns:
            List[VideoSearchResult]: Lista de videos encontrados con título y URL
            
        Raises:
            requests.RequestException: Si hay error en la llamada a la API
            KeyError: Si la respuesta de la API no tiene el formato esperado
            
        Comportamiento:
            1. Obtiene la API key desde variables de entorno
            2. Construye la URL y parámetros para la API de YouTube
            3. Realiza la petición HTTP a la API
            4. Procesa la respuesta y extrae información de cada video
            5. Retorna lista de resultados estructurados
        """
        # Obtener API key desde variables de entorno
        api_key = os.getenv("YOUTUBE_API_KEY")
        
        # Configurar URL y parámetros para la API de YouTube
        url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            "part": "snippet",  # Solicitar información del snippet del video
            "q": keyword,        # Query de búsqueda
            "maxResults": max_results,  # Número máximo de resultados
            "type": "video",     # Solo buscar videos (no canales o playlists)
            "key": api_key       # API key para autenticación
        }
        
        # Realizar petición HTTP a la API de YouTube
        response = requests.get(url, params=params)
        response.raise_for_status()  # Lanzar excepción si hay error HTTP
        
        # Extraer items de la respuesta JSON
        items = response.json().get("items", [])

        # Procesar cada video encontrado
        results = []
        for item in items:
            title = item["snippet"]["title"]  # Título del video
            video_id = item["id"]["videoId"]  # ID único del video
            video_url = f"https://www.youtube.com/watch?v={video_id}"  # Construir URL completa
            
            # Crear objeto de resultado y agregarlo a la lista
            results.append(VideoSearchResult(
                title=title,
                video_url=video_url,
            ))

        return results