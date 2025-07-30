"""
Explicación General:
Este script demuestra el uso básico de LangChain con un modelo de OpenAI.

Muestra cómo enviar mensajes simples y cómo usar una memoria persistente para que el modelo "recuerde" interacciones previas.

Usa FileChatMessageHistory para guardar el historial en disco, lo cual es útil para conservar contexto entre ejecuciones.
"""





# Importa la librería de advertencias y desactiva las advertencias de deprecación específicas de LangChain
import warnings
from langchain._api import LangChainDeprecationWarning
warnings.simplefilter("ignore", category=LangChainDeprecationWarning)

# Carga variables de entorno desde un archivo .env (como la clave de API de OpenAI)
import os
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())
openai_api_key = os.environ["OPENAI_API_KEY"]

# Importa el modelo de chat de OpenAI a través de LangChain
from langchain_openai import ChatOpenAI

# Crea una instancia del chatbot usando el modelo gpt-3.5-turbo
chatbot = ChatOpenAI(model="gpt-3.5-turbo")

# Importa la clase para mensajes del usuario
from langchain_core.messages import HumanMessage

# Envia un mensaje inicial al chatbot
messagesToTheChatbot = [
    HumanMessage(content="My favorite color is blue."),
]

# Ejecuta la conversación y guarda la respuesta
response = chatbot.invoke(messagesToTheChatbot)

# Imprime separadores y mensajes para claridad en la consola
print("\n----------\n")
print("My favorite color is blue.")
print("\n----------\n")
print(response.content)
print("\n----------\n")

# Realiza otra consulta al chatbot basada en el mensaje anterior
response = chatbot.invoke([
    HumanMessage(content="What is my favorite color?")
])

print("\n----------\n")
print("What is my favorite color?")
print("\n----------\n")
print(response.content)
print("\n----------\n")

# Importa herramientas para construir cadenas de lenguaje y manejo de memoria
from langchain import LLMChain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import HumanMessagePromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain.memory import FileChatMessageHistory

# Crea un historial de conversación persistente en un archivo JSON
memory = ConversationBufferMemory(
    chat_memory=FileChatMessageHistory("messages.json"),
    memory_key="messages",
    return_messages=True
)

# Define la plantilla de mensaje para el modelo con historial y nuevo mensaje
prompt = ChatPromptTemplate(
    input_variables=["content", "messages"],
    messages=[
        MessagesPlaceholder(variable_name="messages"),
        HumanMessagePromptTemplate.from_template("{content}")
    ]
)

# Construye una cadena de LLM que utiliza el chatbot, el prompt y la memoria
chain = LLMChain(
    llm=chatbot,
    prompt=prompt,
    memory=memory
)

# Interacción 1: se envía el mensaje "hello!" al chatbot
response = chain.invoke("hello!")
print("\n----------\n")
print("hello!")
print("\n----------\n")
print(response)
print("\n----------\n")

# Interacción 2: se le informa al chatbot el nombre del usuario
response = chain.invoke("my name is Julio")
print("\n----------\n")
print("my name is Julio")
print("\n----------\n")
print(response)
print("\n----------\n")

# Interacción 3: se consulta al chatbot cuál es el nombre del usuario (esperando que recuerde)
response = chain.invoke("what is my name?")
print("\n----------\n")
print("what is my name?")
print("\n----------\n")
print(response)
print("\n----------\n")
