"""
✅ ¿Qué funcionalidades clave muestra este script?
Uso de herramientas (Tavily) con LangChain

Creación de agentes ReAct para razonar paso a paso

Soporte de streaming de tokens

Gestión de memoria por hilo (thread_id) usando MemorySaver

Separación de contexto conversacional con diferentes thread_id


"""



# Cargar variables de entorno desde el archivo .env
import os
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

# Obtener la API key de OpenAI desde las variables de entorno
openai_api_key = os.environ["OPENAI_API_KEY"]

# Importar el modelo de lenguaje de LangChain (usando OpenAI)
from langchain_openai import ChatOpenAI

# Inicializar el modelo LLM con GPT-3.5-Turbo
llm = ChatOpenAI(model="gpt-3.5-turbo")

# Importar herramienta de búsqueda Tavily integrada con LangChain
from langchain_community.tools.tavily_search import TavilySearchResults

# Crear instancia de búsqueda con Tavily, limitando a 2 resultados
search = TavilySearchResults(max_results=2)

# Usar la herramienta de búsqueda directamente con una pregunta
response = search.invoke("Who are the top stars of the 2024 Eurocup?")

# Mostrar la pregunta y la respuesta obtenida por Tavily (búsqueda externa)
print("\n----------\n")
print("Who are the top stars of the 2024 Eurocup?")
print("\n----------\n")
print(response)
print("\n----------\n")

# Preparar herramientas para pasárselas a un agente
tools = [search]

# Asociar herramientas al modelo (modo directo)
llm_with_tools = llm.bind_tools(tools)

# Crear un agente con el patrón ReAct y las herramientas definidas
from langgraph.prebuilt import create_react_agent
agent_executor = create_react_agent(llm, tools)

# Importar el tipo de mensaje humano para pasar como input al agente
from langchain_core.messages import HumanMessage

# Invocar al agente con una pregunta sobre la Eurocopa 2024
response = agent_executor.invoke({"messages": [HumanMessage(content="Where is the soccer Eurocup 2024 played?")]})

# Mostrar la respuesta del agente
print("\n----------\n")
print("Where is the soccer Eurocup 2024 played? (agent)")
print("\n----------\n")
print(response["messages"])
print("\n----------\n")

# Ejecutar el agente en modo streaming con otra pregunta
print("When and where will it be the 2024 Eurocup final match? (agent with streaming)")
print("\n----------\n")
for chunk in agent_executor.stream(
    {"messages": [HumanMessage(content="When and where will it be the 2024 Eurocup final match?")]}
):
    print(chunk)
    print("----")

print("\n----------\n")

# Crear una memoria para guardar el contexto entre invocaciones (simula memoria a largo plazo)
from langgraph.checkpoint.memory import MemorySaver
memory = MemorySaver()

# Crear el agente con soporte de checkpointing/memoria
agent_executor = create_react_agent(llm, tools, checkpointer=memory)

# Usar una configuración con identificador de hilo para mantener el contexto
config = {"configurable": {"thread_id": "001"}}

# Primera pregunta del usuario (hilo 001)
print("Who won the 2024 soccer Eurocup?")
for chunk in agent_executor.stream(
    {"messages": [HumanMessage(content="Who won the 2024 soccer Eurocup?")]}, config
):
    print(chunk)
    print("----")

# Segunda pregunta relacionada, espera que el agente recuerde la anterior
print("Who were the top stars of that winner team?")
for chunk in agent_executor.stream(
    {"messages": [HumanMessage(content="Who were the top stars of that winner team?")]}, config
):
    print(chunk)
    print("----")

# Ahora se cambia de hilo: el agente ya no tiene el contexto anterior
print("(With new thread_id) About what soccer team we were talking?")
config = {"configurable": {"thread_id": "002"}}
for chunk in agent_executor.stream(
    {"messages": [HumanMessage(content="About what soccer team we were talking?")]}, config
):
    print(chunk)
    print("----")
