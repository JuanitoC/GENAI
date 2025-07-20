# rag_chain.py
# Construcción de la cadena RAG (Retrieval-Augmented Generation) usando LangChain, OpenAI y PGVector

import os
from operator import itemgetter
from typing import TypedDict

# Carga de variables de entorno (por ejemplo, claves de API)
from dotenv import load_dotenv
from langchain_community.vectorstores.pgvector import PGVector
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.runnables import RunnableParallel
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import get_buffer_string

# 1. Cargar variables de entorno (API keys, etc.)
load_dotenv()

# 2. Configuración del vector store (PGVector) en PostgreSQL
#    - Aquí se define la conexión a la base de datos vectorial donde se almacenan los embeddings de los documentos (PDFs).
vector_store = PGVector(
    collection_name="collection164",  # Nombre de la colección de vectores
    connection_string="postgresql+psycopg://postgres@localhost:5432/database164",  # Cadena de conexión a la base de datos
    embedding_function=OpenAIEmbeddings()  # Función de embeddings de OpenAI
)

# 3. Definición del prompt para la respuesta final
#    - Este prompt se usará para que el LLM genere una respuesta usando el contexto recuperado.
template = """
Answer given the following context:
{context}

Question: {question}
"""
ANSWER_PROMPT = ChatPromptTemplate.from_template(template)

# 4. Inicialización del modelo de lenguaje (LLM) de OpenAI
llm = ChatOpenAI(temperature=0, model='gpt-4-1106-preview', streaming=True)

# 5. Definición del tipo de entrada para la cadena RAG
class RagInput(TypedDict):
    question: str  # La pregunta del usuario

# 6. Recuperador multi-query
#    - Usa el LLM para generar variantes de la pregunta y recuperar los documentos más relevantes del vector store.
multiquery = MultiQueryRetriever.from_llm(
    retriever=vector_store.as_retriever(),  # Recuperador basado en el vector store
    llm=llm,  # Modelo de lenguaje para generar variantes de la pregunta
)

# 7. Cadena RAG paralela (old_chain)
#    - Primer bloque: Recupera contexto relevante para la pregunta usando el multiquery.
#    - Segundo bloque: Usa el contexto y la pregunta para generar una respuesta con el LLM.
old_chain = (
    RunnableParallel(
        # Recupera contexto relevante para la pregunta
        context=(itemgetter("question") | multiquery),
        # Pasa la pregunta original
        question=itemgetter("question")
    ) |
    RunnableParallel(
        # Genera la respuesta usando el contexto y la pregunta
        answer=(ANSWER_PROMPT | llm),
        # Devuelve los documentos usados como contexto
        docs=itemgetter("context")
    )
).with_types(input_type=RagInput)

# 8. Configuración de la memoria conversacional en PostgreSQL
#    - Permite guardar y recuperar el historial de mensajes de cada sesión de chat.
postgres_memory_url = "postgresql+psycopg://postgres:postgres@localhost:5432/pdf_rag_history"

def get_session_history(session_id):
    """Devuelve el historial de mensajes para una sesión de chat específica."""
    return SQLChatMessageHistory(
        connection_string=postgres_memory_url,
        session_id=session_id
    )

# 9. Prompt para convertir preguntas de seguimiento en preguntas independientes
#    - Si el usuario hace una pregunta de seguimiento, este prompt y cadena la reformulan para que sea autocontenida.
template_with_history = """
Given the following conversation and a follow
up question, rephrase the follow up question
to be a standalone question, in its original
language

Chat History:
{chat_history}
Follow Up Input: {question}
Standalone question:"""

standalone_question_prompt = PromptTemplate.from_template(template_with_history)

# 10. Cadena para obtener la pregunta independiente a partir del historial
#     - Usa el historial de chat y la pregunta de seguimiento para generar una pregunta autocontenida.
standalone_question_mini_chain = RunnableParallel(
    question=RunnableParallel(
        question=RunnablePassthrough(),  # Pasa la pregunta original
        chat_history=lambda x: get_buffer_string(x["chat_history"])  # Convierte el historial a string
    )
    | standalone_question_prompt  # Reformula la pregunta
    | llm                        # Usa el LLM para generar la pregunta autocontenida
    | StrOutputParser()          # Parsea la salida a string
)

# 11. Cadena final con memoria conversacional (final_chain)
#     - Combina la reformulación de preguntas con la cadena RAG.
#     - Usa la memoria conversacional para mantener el contexto entre turnos de chat.
final_chain = RunnableWithMessageHistory(
    runnable=standalone_question_mini_chain | old_chain,  # Encadena la reformulación y la recuperación/generación
    input_messages_key="question",        # Clave de entrada para la pregunta
    history_messages_key="chat_history",  # Clave para el historial de chat
    output_messages_key="answer",         # Clave para la respuesta generada
    get_session_history=get_session_history,  # Función para obtener el historial de la sesión
)

# ---------------------------
# RESUMEN DE FUNCIONAMIENTO
# ---------------------------
# - El usuario hace una pregunta.
# - Si es una pregunta de seguimiento, se reformula para que sea autocontenida usando el historial de chat.
# - Se recuperan los fragmentos de documentos más relevantes usando embeddings y el LLM.
# - Se genera una respuesta usando el contexto recuperado y el LLM.
# - Se guarda el historial de la conversación en PostgreSQL para mantener el contexto.
# - Se devuelven tanto la respuesta como los documentos fuente utilizados.