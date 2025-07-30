"""
Aplicación de Preguntas y Respuestas (QA) sobre un PDF usando LangChain y OpenAI.

Descripción general:
Esta aplicación carga un archivo PDF, lo divide en fragmentos, genera embeddings para cada fragmento y construye un vectorstore para recuperación semántica. Luego, permite hacer preguntas sobre el contenido del PDF utilizando un modelo de lenguaje (LLM) de OpenAI, recuperando los fragmentos más relevantes y generando una respuesta concisa basada en ellos.
"""

import os
# Carga variables de entorno desde un archivo .env (por ejemplo, la API key de OpenAI)
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())
openai_api_key = os.environ["OPENAI_API_KEY"]

# Importa el modelo de lenguaje de OpenAI
from langchain_openai import ChatOpenAI

# Inicializa el modelo de lenguaje (LLM)
llm = ChatOpenAI(model="gpt-3.5-turbo-0125")

# Importa el cargador de PDF de LangChain
from langchain_community.document_loaders import PyPDFLoader

# Ruta al archivo PDF a analizar
file_path = "./data/Be_Good.pdf"

# Carga el PDF y lo convierte en documentos de texto
loader = PyPDFLoader(file_path)
docs = loader.load()

# Importa herramientas para embeddings y vectorstore
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Divide el texto en fragmentos manejables para el procesamiento
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)

# Crea un vectorstore (Chroma) a partir de los fragmentos y sus embeddings
vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())

# Obtiene un recuperador semántico a partir del vectorstore
retriever = vectorstore.as_retriever()

# Importa utilidades para crear cadenas de recuperación y prompts
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

# Define el prompt del sistema para el modelo de lenguaje
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

# Crea la cadena de QA que combina el LLM y el prompt
question_answer_chain = create_stuff_documents_chain(llm, prompt)

# Crea la cadena RAG (retrieval-augmented generation) que une el recuperador y la cadena de QA
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

# Realiza una pregunta sobre el PDF
response = rag_chain.invoke({"input": "What is this article about?"})

print("\n----------\n")
print("What is this article about?")
print("\n----------\n")
print(response["answer"])
print("\n----------\n")
print("\n----------\n")
print("Show metadata:")
print("\n----------\n")
print(response["context"][0].metadata)
print("\n----------\n")