"""
Aplicación de RAG conversacional sobre un archivo de texto usando LangChain y OpenAI.

Descripción general:
Este script implementa un sistema de preguntas y respuestas conversacional sobre un documento de texto. Utiliza un modelo de lenguaje (LLM) de OpenAI, divide el texto en fragmentos, genera embeddings y construye una base de datos vectorial (Chroma) para recuperación semántica. Permite mantener el historial de la conversación, contextualizar preguntas y obtener respuestas precisas basadas en el contenido del documento y el contexto conversacional.
"""

import os
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())
openai_api_key = os.environ["OPENAI_API_KEY"]

from langchain_openai import ChatOpenAI

# Inicializa el modelo de lenguaje de OpenAI
llm = ChatOpenAI(model="gpt-3.5-turbo-0125")

import bs4
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Carga el archivo de texto a analizar
loader = TextLoader("./data/be-good.txt")

# Convierte el archivo en documentos
docs = loader.load()

# Divide el texto en fragmentos manejables
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)

# Crea una base de datos vectorial (Chroma) a partir de los fragmentos y sus embeddings
vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())

# Obtiene un recuperador semántico a partir del vectorstore
retriever = vectorstore.as_retriever()

# Prompt del sistema para el modelo de lenguaje
system_prompt = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer "
    "the question. If you don't know the answer, say that you "
    "don't know. Use three sentences maximum and keep the "
    "answer concise."
    "\n\n"
    "{context}"
)

# Crea el prompt de chat combinando instrucciones del sistema y la pregunta del usuario
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

# Cadena de QA que combina el LLM y el prompt
question_answer_chain = create_stuff_documents_chain(llm, prompt)

# Cadena RAG básica: recupera contexto relevante y genera la respuesta
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

# Realiza una pregunta sobre el texto
response = rag_chain.invoke({"input": "What is this article about?"})

print("\n----------\n")
print("What is this article about?")
print("\n----------\n")
print(response["answer"])
print("\n----------\n")

# Realiza una segunda pregunta, sin historial de conversación
response = rag_chain.invoke({"input": "What was my previous question about?"})

print("\n----------\n")
print("What was my previous question about?")
print("\n----------\n")
print(response["answer"])
print("\n----------\n")

# --- Conversational RAG con historial de chat ---
from langchain.chains import create_history_aware_retriever
from langchain_core.prompts import MessagesPlaceholder

# Prompt para contextualizar preguntas usando el historial
contextualize_q_system_prompt = (
    "Given a chat history and the latest user question "
    "which might reference context in the chat history, "
    "formulate a standalone question which can be understood "
    "without the chat history. Do NOT answer the question, "
    "just reformulate it if needed and otherwise return it as is."
)

contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

# Recuperador que tiene en cuenta el historial de la conversación
history_aware_retriever = create_history_aware_retriever(
    llm, retriever, contextualize_q_prompt
)

from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

# Prompt de QA que incluye el historial de chat
qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

# Cadena RAG que utiliza el recuperador con historial
rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

from langchain_core.messages import AIMessage, HumanMessage

chat_history = []

# Primera pregunta
question = "What is this article about?"
ai_msg_1 = rag_chain.invoke({"input": question, "chat_history": chat_history})

# Actualiza el historial de chat
chat_history.extend(
    [
        HumanMessage(content=question),
        AIMessage(content=ai_msg_1["answer"]),
    ]
)

# Segunda pregunta, ahora con historial
second_question = "What was my previous question about?"
response = rag_chain.invoke({"input": second_question, "chat_history": chat_history})

print("\n----------\n")
print("What was my previous question about?")
print("\n----------\n")
print(response["answer"])
print("\n----------\n")

# --- Manejo de historial de conversación por sesión ---
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    """Obtiene o crea el historial de mensajes para una sesión dada."""
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

# Cadena RAG conversacional con manejo de sesiones
conversational_rag_chain = RunnableWithMessageHistory(
    rag_chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
    output_messages_key="answer",
)

# Realiza preguntas en una sesión identificada
response = conversational_rag_chain.invoke(
    {"input": "What is this article about?"},
    config={
        "configurable": {"session_id": "001"}
    },  # construye una clave "001" en `store`.
)

print("\n----------\n")
print("What is this article about?")
print("\n----------\n")
print(response["answer"])
print("\n----------\n")

response = conversational_rag_chain.invoke(
    {"input": "What was my previous question about?"},
    config={"configurable": {"session_id": "001"}},
)

print("\n----------\n")
print("What was my previous question about?")
print("\n----------\n")
print(response["answer"])
print("\n----------\n")

print("\n----------\n")
print("Conversation History:")
print("\n----------\n")

# Muestra el historial de la conversación de la sesión "001"
for message in store["001"].messages:
    if isinstance(message, AIMessage):
        prefix = "AI"
    else:
        prefix = "User"
    print(f"{prefix}: {message.content}\n")

print("\n----------\n")