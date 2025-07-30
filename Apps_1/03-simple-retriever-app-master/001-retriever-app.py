"""
Este código construye un sistema RAG básico que:

Indexa documentos históricos con embeddings.

Permite búsquedas semánticas.

Combina los resultados con un LLM (GPT-3.5) para responder preguntas contextuales de forma precisa.
"""

# Importa librerías para manejar variables de entorno
import os
from dotenv import load_dotenv, find_dotenv

# Carga las variables del archivo .env (como la clave API de OpenAI)
_ = load_dotenv(find_dotenv())
openai_api_key = os.environ["OPENAI_API_KEY"]  # Accede a la clave desde el entorno

# Importa el modelo de lenguaje de OpenAI a través de LangChain
from langchain_openai import ChatOpenAI

# Inicializa el modelo de lenguaje GPT-3.5 Turbo
llm = ChatOpenAI(model="gpt-3.5-turbo")

# Importa la clase Document para estructurar texto y metadatos
from langchain_core.documents import Document

# Define una lista de documentos relacionados con la familia Kennedy
documents = [
    Document(
        page_content="John F. Kennedy served as the 35th president of the United States from 1961 until his assassination in 1963.",
        metadata={"source": "us-presidents-doc"},
    ),
    Document(
        page_content="Robert F. Kennedy was a key political figure and served as the U.S. Attorney General; he was also assassinated in 1968.",
        metadata={"source": "us-politics-doc"},
    ),
    Document(
        page_content="The Kennedy family is known for their significant influence in American politics and their extensive philanthropic efforts.",
        metadata={"source": "kennedy-family-doc"},
    ),
    Document(
        page_content="Edward M. Kennedy, often known as Ted Kennedy, was a U.S. Senator who played a major role in American legislation over several decades.",
        metadata={"source": "us-senators-doc"},
    ),
    Document(
        page_content="Jacqueline Kennedy Onassis, wife of John F. Kennedy, was an iconic First Lady known for her style, poise, and dedication to cultural and historical preservation.",
        metadata={"source": "first-lady-doc"},
    ),
]

# Importa Chroma (almacén vectorial) y el generador de embeddings de OpenAI
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

# Crea un almacén vectorial con los documentos y embeddings
vectorstore = Chroma.from_documents(
    documents,
    embedding=OpenAIEmbeddings(),
)

# Realiza una búsqueda semántica con la palabra clave "John"
response = vectorstore.similarity_search("John")
print("\n----------\n")
print("Search for John in the vector database:")
print("\n----------\n")
print(response)
print("\n----------\n")

# Realiza la misma búsqueda pero también devuelve el puntaje de similitud
response = vectorstore.similarity_search_with_score("John")
print("\n----------\n")
print("Search for John in the vector database (with scores):")
print("\n----------\n")
print(response)
print("\n----------\n")

# Convierte el vectorstore en un recuperador con búsqueda por similitud (top 1 resultado)
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 1},
)

# Usa el retriever para buscar documentos relevantes para "John" y "Robert"
response = retriever.batch(["John", "Robert"])
print("\n----------\n")
print("Search for John and Robert in the vector database (with vectorstore as retriever):")
print("\n----------\n")
print(response)
print("\n----------\n")

# Alternativa: Define un retriever con una función lambda personalizada
from typing import List
from langchain_core.documents import Document
from langchain_core.runnables import RunnableLambda

# Crea un retriever que busca solo 1 resultado por término
retriever = RunnableLambda(vectorstore.similarity_search).bind(k=1)

# Busca documentos relevantes para "John" y "Robert"
response = retriever.batch(["John", "Robert"])
print("\n----------\n")
print("Search for John and Robert in the vector database (select top result):")
print("\n----------\n")
print(response)
print("\n----------\n")

# Importa herramientas para crear prompts y conectar etapas del pipeline
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

# Define un prompt que obliga al modelo a responder solo usando el contexto
message = """
Answer this question using the provided context only.

{question}

Context:
{context}
"""

# Crea una plantilla de prompt para el modelo de lenguaje
prompt = ChatPromptTemplate.from_messages([("human", message)])

# Construye una cadena: recuperación → construcción de prompt → generación de respuesta
chain = {
    "context": retriever, 
    "question": RunnablePassthrough()
} | prompt | llm

# Ejecuta la cadena con una consulta sobre Jacqueline Kennedy
response = chain.invoke("tell me about Jackie")
print("\n----------\n")
print("tell me about Jackie (simple retriever):")
print("\n----------\n")
print(response.content)
print("\n----------\n")
