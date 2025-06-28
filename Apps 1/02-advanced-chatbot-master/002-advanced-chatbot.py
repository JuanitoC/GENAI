"""
🧠 Resumen de lo que hace este script:
Usa LangChain + OpenAI GPT para interactuar con un chatbot.

Permite manejar memoria por sesión, como si tuvieras múltiples usuarios o sesiones independientes.

Muestra la diferencia entre:

Un chatbot sin memoria (inicial).

Un chatbot con memoria persistente por sesión.

Un chatbot con memoria limitada a los últimos mensajes (simulando olvido).
"""

# Ignora las advertencias de deprecación específicas de LangChain
import warnings
from langchain._api import LangChainDeprecationWarning
warnings.simplefilter("ignore", category=LangChainDeprecationWarning)

# Carga las variables de entorno desde un archivo .env
import os
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())  # Carga el archivo .env automáticamente
openai_api_key = os.environ["OPENAI_API_KEY"]  # Obtiene la clave de API

# Crea un chatbot con el modelo GPT-3.5-Turbo usando LangChain
from langchain_openai import ChatOpenAI
chatbot = ChatOpenAI(model="gpt-3.5-turbo")

# Importa clase para representar mensajes del usuario
from langchain_core.messages import HumanMessage

# Primer mensaje al chatbot
messagesToTheChatbot = [
    HumanMessage(content="My favorite color is blue."),
]

# Envía el mensaje y recibe respuesta
response = chatbot.invoke(messagesToTheChatbot)

# Muestra mensaje original y respuesta del chatbot
print("\n----------\n")
print("My favorite color is blue.")
print("\n----------\n")
print(response.content)
print("\n----------\n")

# Segunda interacción: pregunta por el color favorito
response = chatbot.invoke([
    HumanMessage(content="What is my favorite color?")
])
print("\n----------\n")
print("What is my favorite color?")
print("\n----------\n")
print(response.content)
print("\n----------\n")

# ---- Sección: Chat con historial de mensajes gestionado manualmente ----

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# Diccionario en memoria para guardar sesiones de chat
chatbotMemory = {}

# Función para obtener o crear historial para una sesión específica
def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in chatbotMemory:
        chatbotMemory[session_id] = ChatMessageHistory()
    return chatbotMemory[session_id]

# Crea un chatbot con historial de mensajes por sesión
chatbot_with_message_history = RunnableWithMessageHistory(
    chatbot, 
    get_session_history
)

# Define la primera sesión con ID "001"
session1 = {"configurable": {"session_id": "001"}}

# Envía un mensaje en la sesión 1
responseFromChatbot = chatbot_with_message_history.invoke(
    [HumanMessage(content="My favorite color is red.")],
    config=session1,
)
print("\n----------\n")
print("My favorite color is red.")
print("\n----------\n")
print(responseFromChatbot.content)
print("\n----------\n")

# Pregunta por el color favorito dentro de la misma sesión (debería recordar "red")
responseFromChatbot = chatbot_with_message_history.invoke(
    [HumanMessage(content="What's my favorite color?")],
    config=session1,
)
print("\n----------\n")
print("What's my favorite color? (in session1)")
print("\n----------\n")
print(responseFromChatbot.content)
print("\n----------\n")

# Segunda sesión con ID diferente
session2 = {"configurable": {"session_id": "002"}}

# Pregunta por el color favorito en una sesión nueva (no debería recordar nada)
responseFromChatbot = chatbot_with_message_history.invoke(
    [HumanMessage(content="What's my favorite color?")],
    config=session2,
)
print("\n----------\n")
print("What's my favorite color? (in session2)")
print("\n----------\n")
print(responseFromChatbot.content)
print("\n----------\n")

# Regresa a sesión1 y vuelve a preguntar
responseFromChatbot = chatbot_with_message_history.invoke(
    [HumanMessage(content="What's my favorite color?")],
    config=session1,
)
print("\n----------\n")
print("What's my favorite color? (in session1 again)")
print("\n----------\n")
print(responseFromChatbot.content)
print("\n----------\n")

# Añade información a la sesión2
responseFromChatbot = chatbot_with_message_history.invoke(
    [HumanMessage(content="Mi name is Julio.")],
    config=session2,
)
print("\n----------\n")
print("Mi name is Julio. (in session2)")
print("\n----------\n")
print(responseFromChatbot.content)
print("\n----------\n")

# Pregunta por el nombre en sesión2 (debería recordar "Julio")
responseFromChatbot = chatbot_with_message_history.invoke(
    [HumanMessage(content="What is my name?")],
    config=session2,
)
print("\n----------\n")
print("What is my name? (in session2)")
print("\n----------\n")
print(responseFromChatbot.content)
print("\n----------\n")

# Confusión: se vuelve a usar sesión1 pero el comentario dice "session2"
responseFromChatbot = chatbot_with_message_history.invoke(
    [HumanMessage(content="What is my favorite color?")],
    config=session1,
)
print("\n----------\n")
print("What is my favorite color? (in session2)")  # ¡Este comentario parece incorrecto!
print("\n----------\n")
print(responseFromChatbot.content)
print("\n----------\n")

# ---- Sección: Chat con memoria limitada (solo últimos mensajes) ----

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough

# Función para limitar la memoria a los últimos N mensajes
def limited_memory_of_messages(messages, number_of_messages_to_keep=2):
    return messages[-number_of_messages_to_keep:]

# Plantilla con un sistema y mensajes del usuario
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant. Answer all questions to the best of your ability.",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

# Cadena que limita los mensajes y aplica el prompt antes de invocar el chatbot
limitedMemoryChain = (
    RunnablePassthrough.assign(messages=lambda x: limited_memory_of_messages(x["messages"]))
    | prompt 
    | chatbot
)

# Crea una versión del chatbot con memoria limitada y sesiones
chatbot_with_limited_message_history = RunnableWithMessageHistory(
    limitedMemoryChain,
    get_session_history,
    input_messages_key="messages",
)

# Se sigue usando la sesión1, agregando nuevos mensajes
responseFromChatbot = chatbot_with_message_history.invoke(
    [HumanMessage(content="My favorite vehicles are Vespa scooters.")],
    config=session1,
)
print("\n----------\n")
print("My favorite vehicles are Vespa scooters. (in session1)")
print("\n----------\n")
print(responseFromChatbot.content)
print("\n----------\n")

responseFromChatbot = chatbot_with_message_history.invoke(
    [HumanMessage(content="My favorite city is San Francisco.")],
    config=session1,
)
print("\n----------\n")
print("My favorite city is San Francisco. (in session1)")
print("\n----------\n")
print(responseFromChatbot.content)
print("\n----------\n")

# Pregunta al chatbot con memoria limitada (últimos 2 mensajes) — puede que ya no recuerde el color
responseFromChatbot = chatbot_with_limited_message_history.invoke(
    {
        "messages": [HumanMessage(content="what is my favorite color?")],
    },
    config=session1,
)
print("\n----------\n")
print("what is my favorite color? (chatbot with memory limited to the last 3 messages)")
print("\n----------\n")
print(responseFromChatbot.content)
print("\n----------\n")

# Pregunta al chatbot con memoria completa — debería recordar
responseFromChatbot = chatbot_with_message_history.invoke(
    [HumanMessage(content="what is my favorite color?")],
    config=session1,
)
print("\n----------\n")
print("what is my favorite color? (chatbot with unlimited memory)")
print("\n----------\n")
print(responseFromChatbot.content)
print("\n----------\n")
