"""
RESUMEN DEL ARCHIVO:
Este archivo define los agentes de inteligencia artificial utilizados en el sistema
de investigación multiagente. Los agentes están diseñados para realizar investigaciones
especializadas sobre tecnologías en diferentes áreas de negocio.

Arquitectura de Agentes:
- Research Manager: Coordina y agrega resultados de múltiples investigaciones
- Research Agent: Realiza investigaciones específicas sobre tecnologías y áreas de negocio

Características principales:
- Integración con OpenAI GPT-4 Turbo
- Herramientas de búsqueda web (SerperDev) y YouTube
- Roles y objetivos bien definidos para cada agente
- Capacidad de delegación entre agentes
- Configuración de verbosidad para debugging

Los agentes trabajan en conjunto para encontrar artículos de blog y videos de YouTube
relevantes sobre tecnologías específicas en diferentes áreas de negocio.
"""

from typing import List
from crewai import Agent
from langchain_openai import ChatOpenAI
from crewai_tools import SerperDevTool
from tools.youtube_search_tools import YoutubeVideoSearchTool


class ResearchAgents():
    """
    Clase que define y configura los agentes de investigación para el sistema multiagente.
    
    Esta clase encapsula la creación y configuración de agentes especializados
    que pueden realizar investigaciones sobre tecnologías en diferentes áreas de negocio.
    Cada agente tiene herramientas específicas y objetivos bien definidos.
    """

    def __init__(self):
        """
        Inicializa la clase ResearchAgents configurando las herramientas y el modelo LLM.
        
        Configura:
        - Herramienta de búsqueda web (SerperDev)
        - Herramienta de búsqueda de YouTube
        - Modelo de lenguaje OpenAI GPT-4 Turbo
        """
        self.searchInternetTool = SerperDevTool()  # Herramienta para búsquedas web
        self.youtubeSearchTool = YoutubeVideoSearchTool()  # Herramienta para búsquedas en YouTube
        self.llm = ChatOpenAI(model="gpt-4-turbo-preview")  # Modelo de lenguaje avanzado

    def research_manager(self, technologies: List[str], businessareas: List[str]) -> Agent:
        """
        Crea y configura el agente Research Manager.
        
        El Research Manager es responsable de coordinar y agregar los resultados
        de múltiples investigaciones realizadas por Research Agents. Actúa como
        un supervisor que asegura que se complete la investigación para todas las
        combinaciones de tecnologías y áreas de negocio.
        
        Args:
            technologies (List[str]): Lista de tecnologías a investigar
            businessareas (List[str]): Lista de áreas de negocio a investigar
            
        Returns:
            Agent: Agente configurado con rol de Research Manager
            
        Características del agente:
        - Rol: Research Manager
        - Objetivo: Agregar resultados de múltiples investigaciones
        - Herramientas: Búsqueda web y YouTube
        - Capacidad de delegación habilitada
        - Verbosidad activada para debugging
        """
        return Agent(
            role="Research Manager",
            goal=f"""Generate a list of JSON objects containing the urls for 3 recent blog articles and 
                the url and title for 3 recent YouTube videos, for each technology in each business area.
             
                Technologies: {technologies}
                Business Areas: {businessareas}

                Important:
                - The final list of JSON objects must include all technologies and business areas. Do not leave any out.
                - If you can't find information for a specific industry or business area, fill in the information with the word "MISSING".
                - Do not generate fake information. Only return the information you find. Nothing else!
                - Do not stop researching until you find the requested information for each business area in each technology.
                - All the technologies and business areas exist so keep researching until you find the information for each one.
                - Make sure you each researched business area for each technology contains 3 blog articles and 3 YouTube videos.
                """,
            backstory="""As a Research Manager, you are responsible for aggregating all the researched information into a list.""",
            llm=self.llm,
            tools=[self.searchInternetTool, self.youtubeSearchTool], # TODO: Add tools
            verbose=True,
            allow_delegation=True
        )

    def research_agent(self) -> Agent:
        """
        Crea y configura el agente Research Agent.
        
        El Research Agent es responsable de realizar investigaciones específicas
        sobre una tecnología particular en áreas de negocio específicas. Este agente
        se enfoca en encontrar contenido relevante como artículos de blog y videos
        de YouTube sobre la tecnología asignada.
        
        Returns:
            Agent: Agente configurado con rol de Research Agent
            
        Características del agente:
        - Rol: Research Agent
        - Objetivo: Investigar áreas de negocio específicas para una tecnología
        - Herramientas: Búsqueda web y YouTube
        - Enfoque en encontrar contenido real y verificable
        - Verbosidad activada para debugging
        """
        return Agent(
            role="Research Agent",
            goal="""Look up the specific business areas for a given technology and find urls for 3 recent blog articles and 
                the url and title for 3 recent YouTube videos in the specified business area. It is your goal to return this collected 
                information in a JSON object""",
            backstory="""As a Research Agent, you are responsible for looking up specific business areas 
                within a technology and gathering relevant information.
                
                Important:
                - Once you've found the information, immediately stop searching for additional information.
                - Only return the requested information. NOTHING ELSE!
                - Do not generate fake information. Only return the information you find. Nothing else!
                """,
            tools=[self.searchInternetTool, self.youtubeSearchTool], # TODO: Add tools
            llm=self.llm,
            verbose=True
        )