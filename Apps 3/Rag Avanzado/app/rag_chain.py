# rag_chain.py
# Construcción de la cadena RAG (Retrieval-Augmented Generation) usando LangChain, OpenAI y PGVector

import os
from operator import itemgetter
from typing import TypedDict

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

# Cargar variables de entorno (por ejemplo, claves de API)
load_dotenv()

# Configuración del vector store en PostgreSQL usando PGVector
vector_store = PGVector(
    collection_name="collection164",
    connection_string="postgresql+psycopg://postgres@localhost:5432/database164",
    embedding_function=OpenAIEmbeddings()
)

# Plantilla de prompt para la respuesta final
template = """
Answer given the following context:
{context}

Question: {question}
"""

ANSWER_PROMPT = ChatPromptTemplate.from_template(template)

# Inicialización del modelo de lenguaje (LLM) de OpenAI
llm = ChatOpenAI(temperature=0, model='gpt-4-1106-preview', streaming=True)

# Definición del tipo de entrada para la cadena RAG
class RagInput(TypedDict):
    question: str

# Recuperador multi-query para obtener documentos relevantes usando el LLM
multiquery = MultiQueryRetriever.from_llm(
    retriever=vector_store.as_retriever(),
    llm=llm,
)

# Cadena RAG paralela: recupera contexto y genera respuesta
old_chain = (
        RunnableParallel(
            context=(itemgetter("question") | multiquery),
            question=itemgetter("question")
        ) |
        RunnableParallel(
            answer=(ANSWER_PROMPT | llm),
            docs=itemgetter("context")
        )
).with_types(input_type=RagInput)

# Configuración de la memoria conversacional en PostgreSQL
postgres_memory_url = "postgresql+psycopg://postgres:postgres@localhost:5432/pdf_rag_history"

get_session_history = lambda session_id: SQLChatMessageHistory(
    connection_string=postgres_memory_url,
    session_id=session_id
)

# Prompt para convertir preguntas de seguimiento en preguntas independientes
# usando el historial de chat
template_with_history="""
Given the following conversation and a follow
up question, rephrase the follow up question
to be a standalone question, in its original
language

Chat History:
{chat_history}
Follow Up Input: {question}
Standalone question:"""

standalone_question_prompt = PromptTemplate.from_template(template_with_history)

# Cadena para obtener la pregunta independiente a partir del historial
standalone_question_mini_chain = RunnableParallel(
    question=RunnableParallel(
        question=RunnablePassthrough(),
        chat_history=lambda x:get_buffer_string(x["chat_history"])
    )
    | standalone_question_prompt
    | llm
    | StrOutputParser()
)

# Cadena final con memoria conversacional
final_chain = RunnableWithMessageHistory(
    runnable=standalone_question_mini_chain | old_chain,
    input_messages_key="question",
    history_messages_key="chat_history",
    output_messages_key="answer",
    get_session_history=get_session_history,
)