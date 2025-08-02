"""
RESUMEN DEL ARCHIVO:
Este archivo implementa la clase TechnologyResearchCrew que coordina el sistema
multiagente de investigación. La crew actúa como el orquestador principal que
configura agentes, tareas y ejecuta el flujo de investigación completo.

Arquitectura de la Crew:
- Configuración de agentes (Research Manager y Research Agent)
- Creación de tareas de investigación específicas por tecnología
- Tarea de gestión para agregar resultados
- Ejecución coordinada del flujo completo

Características principales:
- Integración con OpenAI GPT-4 Turbo
- Configuración dinámica basada en tecnologías y áreas de negocio
- Sistema de logging de eventos
- Manejo de errores robusto
- Verbosidad configurada para debugging

La crew es responsable de ejecutar investigaciones completas sobre múltiples
tecnologías en diferentes áreas de negocio, generando un dataset estructurado
de contenido relevante.
"""

from langchain_openai import ChatOpenAI
from log_manager import append_event
from agents import ResearchAgents
from tasks import ResearchTasks
from crewai import Crew

class TechnologyResearchCrew:
    """
    Clase principal que coordina el sistema multiagente de investigación.
    
    Esta clase actúa como el orquestador principal del sistema, configurando
    agentes, tareas y ejecutando el flujo completo de investigación. Es responsable
    de coordinar la investigación de múltiples tecnologías en diferentes áreas de negocio.
    """

    def __init__(self, input_id: str):
        """
        Inicializa la crew con un identificador único y configura el modelo LLM.
        
        Args:
            input_id (str): Identificador único para rastrear esta investigación
        """
        self.input_id = input_id
        self.crew = None  # Crew se inicializa en setup_crew
        self.llm = ChatOpenAI(model="gpt-4-turbo-preview")  # Modelo de lenguaje avanzado

    def setup_crew(self, technologies: list[str], businessareas: list[str]):
        """
        Configura la crew con agentes y tareas basados en las tecnologías y áreas de negocio.
        
        Este método es el corazón de la configuración del sistema multiagente.
        Crea los agentes necesarios, configura las tareas de investigación
        específicas para cada tecnología, y establece la tarea de gestión
        que coordina todos los resultados.
        
        Args:
            technologies (list[str]): Lista de tecnologías a investigar
            businessareas (list[str]): Lista de áreas de negocio a investigar
            
        Flujo de configuración:
        1. Crear agentes (Research Manager y Research Agent)
        2. Crear tareas de investigación específicas por tecnología
        3. Crear tarea de gestión para agregar resultados
        4. Configurar la crew con agentes y tareas
        """
        print(f"""Setting up crew for
        {self.input_id} with technologies {technologies}
        and businessareas {businessareas}""")

        # PASO 1: CONFIGURAR AGENTES
        agents = ResearchAgents()

        # Crear agente Research Manager para coordinar resultados
        research_manager = agents.research_manager(technologies, businessareas)
        # Crear agente Research Agent para investigaciones específicas
        research_agent = agents.research_agent()
  
        # PASO 2: CONFIGURAR TAREAS
        tasks = ResearchTasks(input_id=self.input_id)

        # Crear tareas de investigación específicas para cada tecnología
        # Cada tecnología tendrá su propia tarea de investigación
        technology_research_tasks = [
            tasks.technology_research(research_agent, technology, businessareas)
            for technology in technologies
        ]

        # Crear tarea de gestión que coordina todos los resultados
        manage_research_task = tasks.manage_research(
            research_manager, technologies, businessareas, technology_research_tasks)
        
        # PASO 3: CREAR CREW
        # La crew se configura con todos los agentes y tareas
        self.crew = Crew(
            agents=[research_manager, research_agent],  # Agentes disponibles
            tasks=[*technology_research_tasks, manage_research_task],  # Todas las tareas
            verbose=2,  # Verbosidad alta para debugging
            )

    def kickoff(self):
        """
        Ejecuta la crew y realiza la investigación completa.
        
        Este método inicia el proceso de investigación multiagente,
        ejecutando todas las tareas configuradas y coordinando los
        resultados entre los agentes.
        
        Returns:
            str: Resultado de la investigación o mensaje de error
            
        Flujo de ejecución:
        1. Verificar que la crew esté configurada
        2. Registrar inicio de la investigación
        3. Ejecutar la crew con todas las tareas
        4. Registrar finalización o error
        5. Retornar resultados
        """
        if not self.crew:
            print(f"""Crew not found for 
            {self.input_id}""")
            return
        
        # Registrar inicio de la investigación
        append_event(self.input_id, "CREW STARTED")
        
        try:
            print(f"""Running crew for 
            {self.input_id}""")
            # Ejecutar la crew con todas las tareas configuradas
            results = self.crew.kickoff()
            # Registrar finalización exitosa
            append_event(self.input_id, "CREW COMPLETED")
            return results

        except Exception as e:
            # Registrar error si algo falla
            append_event(self.input_id, "CREW FAILED")
            return str(e)