"""
Descripción técnica:

Este script implementa una arquitectura multiagente basada en grafos de estado utilizando LangChain, LangGraph y modelos LLM de OpenAI. El objetivo es orquestar un flujo de trabajo colaborativo entre agentes especializados en tareas de marketing de contenidos, simulando la dinámica de un equipo real.

Componentes principales:
- **Agentes (Agents):** Cada agente es una instancia de un ejecutor (`AgentExecutor`) parametrizado con un prompt de sistema y un conjunto de herramientas (tools). Los agentes implementados son:
    - `online_researcher`: realiza búsquedas web y extracción de información.
    - `blog_manager`: transforma borradores en artículos optimizados para SEO.
    - `social_media_manager`: sintetiza el contenido en mensajes para redes sociales.
- **Herramientas (Tools):** Se integran herramientas externas como TavilySearchResults (búsqueda web) y un parser HTML basado en BeautifulSoup, expuestas como funciones decoradas con `@tool` para su uso por los agentes.
- **Gestor de flujo (Content Marketing Manager):** Un agente especial que actúa como router, decidiendo dinámicamente qué agente debe ejecutar la siguiente acción, o cuándo finalizar el proceso. Utiliza funciones OpenAI para ruteo y toma de decisiones.
- **Grafo de estados (StateGraph):** El flujo de trabajo se modela como un grafo dirigido, donde los nodos son agentes y las transiciones (edges) dependen de la salida del gestor de flujo. El grafo es compilado y ejecutado con un límite de recursión para evitar bucles infinitos.

Dependencias clave:
- `langchain`, `langchain_openai`, `langchain_community`, `langgraph`: para la definición de agentes, herramientas, prompts y grafos de estado.
- `openai`: acceso a modelos LLM (GPT-4 Turbo Preview).
- `python-dotenv`: gestión de variables de entorno y claves API.
- `beautifulsoup4`, `requests`: scraping y procesamiento de HTML.

El diseño es modular y extensible, permitiendo añadir nuevos roles/agentes, herramientas o modificar la lógica de ruteo. Es un ejemplo avanzado de integración de LLMs con flujos multiagente y herramientas externas, adecuado para prototipos de automatización de procesos complejos basados en IA generativa.
"""
# Importación de librerías necesarias para manejo de variables de entorno y API de OpenAI
import os
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())
openai_api_key = os.environ["OPENAI_API_KEY"]

# Importación del modelo de lenguaje de OpenAI
from langchain_openai import ChatOpenAI

# Inicialización del modelo LLM de OpenAI
llm = ChatOpenAI(model="gpt-4-turbo-preview")

# Importaciones adicionales para utilidades y manejo de advertencias
import functools
import operator
import requests
import os
import warnings

# Ignorar advertencias específicas de sintaxis
warnings.filterwarnings("ignore", category=SyntaxWarning, message="invalid escape sequence")

from dotenv import load_dotenv
from bs4 import BeautifulSoup

from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.messages import HumanMessage, BaseMessage
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from langgraph.graph import StateGraph, END
from langchain.tools import tool
from langchain_openai import ChatOpenAI

from typing import TypedDict, Annotated, Sequence

from langchain_community.tools.tavily_search import TavilySearchResults

# Cargar variables de entorno
load_dotenv()

# Definición de herramienta personalizada para procesar contenido web
@tool("process_search_tool", return_direct=False)
def process_search_tool(url: str) -> str:
    """Parsea el contenido web usando BeautifulSoup"""
    response = requests.get(url=url)
    soup = BeautifulSoup(response.content, "html.parser")
    return soup.get_text()

# Lista de herramientas disponibles para los agentes
tools = [TavilySearchResults(max_results=1), process_search_tool]

# Función para crear un nuevo agente con un prompt y herramientas específicas
def create_new_agent(llm: ChatOpenAI,
                  tools: list,
                  system_prompt: str) -> AgentExecutor:
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="messages"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ])

    agent = create_openai_tools_agent(llm, tools, prompt)
    executor = AgentExecutor(agent=agent, tools=tools)
    return executor

# Función para ejecutar un nodo de agente y devolver el mensaje generado
def agent_node(state, agent, name):
    result = agent.invoke(state)
    return {"messages": [HumanMessage(content=result["output"], name=name)]}

# Definición de los roles del equipo de marketing de contenidos
content_marketing_team = ["online_researcher", "blog_manager", "social_media_manager"]

# Prompt del sistema para el manager de marketing de contenidos
system_prompt = (
    "Como gerente de marketing de contenidos, tu rol es supervisar la interacción entre estos "
    "trabajadores: {content_marketing_team}. Según la solicitud del usuario, "
    "determina qué trabajador debe tomar la siguiente acción. Cada trabajador es responsable de "
    "ejecutar una tarea específica y reportar sus hallazgos y progreso. "
    "Una vez que todas las tareas estén completadas, indica 'FINISH'."
)

# Opciones posibles para el flujo de trabajo
options = ["FINISH"] + content_marketing_team

# Definición de la función de ruteo para decidir el siguiente rol
function_def = {
    "name": "route",
    "description": "Selecciona el siguiente rol.",
    "parameters": {
        "title": "routeSchema",
        "type": "object",
        "properties": {"next": {"title": "Next", "anyOf": [{"enum": options}]}},
        "required": ["next"]
    }
}

# Prompt para decidir el siguiente paso en el flujo de trabajo
prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="messages"),
    ("system",
     "Dada la conversación anterior, ¿quién debe actuar a continuación? ¿O debemos FINALIZAR? Selecciona uno de: {options}"),
]).partial(options=str(options), content_marketing_team=", ".join(content_marketing_team))

# Cadena de decisión del gerente de marketing de contenidos
content_marketing_manager_chain = (prompt | llm.bind_functions(
    functions=[function_def], function_call="route") | JsonOutputFunctionsParser())

# Definición del agente de investigación online
online_researcher_agent = create_new_agent(
    llm,
    tools,
    """Tu rol principal es funcionar como un asistente inteligente de investigación online, capaz de buscar las últimas y más relevantes historias de tendencia en sectores como política, tecnología, salud, cultura y eventos globales. Puedes acceder a una amplia gama de fuentes de noticias, blogs y redes sociales para recopilar información en tiempo real."""
)

# Nodo parcial para el investigador online
online_researcher_node = functools.partial(
    agent_node, agent=online_researcher_agent, name="online_researcher"
)

# Definición del agente gestor de blog
blog_manager_agent = create_new_agent(
    llm, tools,
    """Eres un Gestor de Blog. Tu rol abarca responsabilidades críticas para transformar borradores iniciales en artículos de blog pulidos y optimizados para SEO que atraigan y hagan crecer la audiencia. Comenzando con borradores proporcionados por investigadores online, debes asegurar que el contenido se alinee con el tono, audiencia y objetivos temáticos del blog. Tus responsabilidades incluyen: mejora de contenido, optimización SEO, cumplimiento de buenas prácticas, supervisión editorial y análisis de métricas para mejorar la estrategia del blog."""
)

# Nodo parcial para el gestor de blog
blog_manager_node = functools.partial(
    agent_node, agent=blog_manager_agent, name="blog_manager")

# Definición del agente gestor de redes sociales
social_media_manager_agent = create_new_agent(
    llm, tools,
    """Eres un Gestor de Redes Sociales. Tu rol, especialmente para Twitter, implica transformar borradores de investigación en tweets concisos y atractivos que resuenen con la audiencia y sigan las mejores prácticas de la plataforma. Debes condensar el mensaje, optimizar el engagement y cumplir con las normas de la plataforma."""
)

# Nodo parcial para el gestor de redes sociales
social_media_manager_node = functools.partial(
    agent_node, agent=social_media_manager_agent, name="social_media_manager")

# Definición del estado del agente para el grafo
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    next: str
    
# Creación del grafo de estados para el flujo multiagente
workflow = StateGraph(AgentState)

# Agregar nodos al grafo para cada rol
workflow.add_node("content_marketing_manager", content_marketing_manager_chain)
workflow.add_node("online_researcher", online_researcher_node)
workflow.add_node("blog_manager", blog_manager_node)
workflow.add_node("social_media_manager", social_media_manager_node)

# Definir transiciones de cada miembro hacia el manager
for member in content_marketing_team:
    workflow.add_edge(start_key=member, end_key="content_marketing_manager")

# Mapeo condicional para decidir el siguiente nodo
conditional_map = {k: k for k in content_marketing_team}

conditional_map['FINISH'] = END

# Agregar transiciones condicionales desde el manager
workflow.add_conditional_edges(
    "content_marketing_manager", lambda x: x["next"], conditional_map)

# Definir el punto de entrada del flujo
workflow.set_entry_point("content_marketing_manager")

# Compilar el flujo multiagente
multiagent = workflow.compile()

# Ejecución del flujo multiagente con un ejemplo de solicitud
for s in multiagent.stream(
    {
        "messages": [
            HumanMessage(
                content="""Escríbeme un informe sobre el Comportamiento Agéntico. Después de la investigación, pasa los hallazgos al gestor de blog para generar el artículo final. Una vez hecho, pásalo al gestor de redes sociales para escribir un tweet sobre el tema."""
            )
        ],
    },
    # Número máximo de pasos en el flujo multiagente
    {"recursion_limit": 150}
):
    if not "__end__" in s:
        print(s, end="\n\n-----------------\n\n")
