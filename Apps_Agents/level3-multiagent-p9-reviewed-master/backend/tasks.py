"""
RESUMEN DEL ARCHIVO:
Este archivo define las tareas que serán ejecutadas por los agentes en el sistema
multiagente de investigación. Las tareas están diseñadas para investigar tecnologías
específicas en diferentes áreas de negocio, encontrando artículos de blog y videos
de YouTube relevantes.

Arquitectura de Tareas:
- Technology Research Task: Investigación específica de una tecnología en múltiples áreas
- Manage Research Task: Coordinación y agregación de resultados de múltiples investigaciones

Características principales:
- Integración con CrewAI Task framework
- Callbacks para logging de eventos
- Configuración de salida JSON estructurada
- Ejecución asíncrona para tareas de investigación
- Validación de datos con modelos Pydantic

Las tareas trabajan en conjunto para generar un dataset completo de contenido
relevante sobre tecnologías en diferentes áreas de negocio.
"""

from crewai import Task, Agent
from textwrap import dedent


from log_manager import append_event
from models import BusinessareaInfo, BusinessareaInfoList


class ResearchTasks():
    """
    Clase que define las tareas de investigación para el sistema multiagente.
    
    Esta clase encapsula la creación y configuración de tareas especializadas
    que serán ejecutadas por los agentes para realizar investigaciones sobre
    tecnologías en diferentes áreas de negocio.
    """

    def __init__(self, input_id):
        """
        Inicializa la clase ResearchTasks con un identificador único.
        
        Args:
            input_id (str): Identificador único para rastrear esta investigación
        """
        self.input_id = input_id

    def append_event_callback(self, task_output):
        """
        Callback que se ejecuta cuando una tarea completa su trabajo.
        
        Este método se utiliza para registrar el progreso de las tareas
        en el sistema de logging, permitiendo rastrear el estado de la
        investigación en tiempo real.
        
        Args:
            task_output: Resultado de la tarea completada
        """
        print(f"Appending event for {self.input_id} with output {task_output}")
        append_event(self.input_id, task_output.exported_output)

    def manage_research(self, agent: Agent, technologies: list[str], businessareas: list[str], tasks: list[Task]):
        """
        Crea una tarea de gestión de investigación que coordina múltiples investigaciones.
        
        Esta tarea actúa como un supervisor que toma los resultados de múltiples
        investigaciones de tecnología y los agrega en un formato estructurado.
        
        Args:
            agent (Agent): Agente que ejecutará la tarea (Research Manager)
            technologies (list[str]): Lista de tecnologías investigadas
            businessareas (list[str]): Lista de áreas de negocio investigadas
            tasks (list[Task]): Lista de tareas de investigación previas
            
        Returns:
            Task: Tarea configurada para gestionar y agregar resultados
            
        Características de la tarea:
        - Descripción detallada del objetivo de agregación
        - Salida esperada en formato JSON estructurado
        - Callback para logging de eventos
        - Contexto de tareas previas para referencia
        - Validación de salida con modelo BusinessareaInfoList
        """
        return Task(
            description=dedent(f"""Based on the list of technologies {technologies} and the business areas {businessareas},
                use the results from the Research Agent to research each business area in each technology.
                to put together a json object containing the URLs for 3 blog articles, the URLs and title 
                for 3 YouTube interviews for each business area in each technology.
                               
                """),
            agent=agent,
            expected_output=dedent(
                """A json object containing the URLs for 3 blog articles and the URLs and 
                    titles for 3 YouTube interviews for each business area in each technology."""),
            callback=self.append_event_callback,
            context=tasks,
            output_json=BusinessareaInfoList
        )

    def technology_research(self, agent: Agent, technology: str, businessareas: list[str]):
        """
        Crea una tarea de investigación específica para una tecnología.
        
        Esta tarea se enfoca en investigar una tecnología particular en múltiples
        áreas de negocio, encontrando artículos de blog y videos de YouTube relevantes.
        
        Args:
            agent (Agent): Agente que ejecutará la tarea (Research Agent)
            technology (str): Tecnología específica a investigar
            businessareas (list[str]): Lista de áreas de negocio para investigar
            
        Returns:
            Task: Tarea configurada para investigación de tecnología específica
            
        Características de la tarea:
        - Descripción detallada con estrategias de búsqueda
        - Ejecución asíncrona para mejor rendimiento
        - Callback para logging de eventos
        - Validación de salida con modelo BusinessareaInfo
        - Enfoque en encontrar información real y verificable
        """
        return Task(
            description=dedent(f"""Research the business areas {businessareas} for the {technology} technology. 
                For each business area, find the URLs for 3 recent blog articles and the URLs and titles for
                3 recent YouTube videos in each business area.
                Return this collected information in a JSON object.
                               
                Helpful Tips:
                - To find the blog articles names and URLs, perform searches on Google such like the following:
                    - "{technology} [BUSINESS AREA HERE] blog articles"
                - To find the youtube videos, perform searches on YouTube such as the following:
                    - "{technology} in [BUSINESS AREA HERE]"
                               
                Important:
                - Once you've found the information, immediately stop searching for additional information.
                - Only return the requested information. NOTHING ELSE!
                - Do not generate fake information. Only return the information you find. Nothing else!
                - Do not stop researching until you find the requested information for each business area in the technology.
                """),
            agent=agent,
            expected_output="""A JSON object containing the researched information for each business area in the technology.""",
            callback=self.append_event_callback,
            output_json=BusinessareaInfo,
            async_execution=True
        )