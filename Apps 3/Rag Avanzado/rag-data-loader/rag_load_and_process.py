# rag_load_and_process.py
# Script para cargar, procesar y vectorizar PDFs usando LangChain y PGVector

import os

from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, UnstructuredPDFLoader
from langchain_community.vectorstores.pgvector import PGVector
from langchain_experimental.text_splitter import SemanticChunker
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings

# Cargar variables de entorno (por ejemplo, claves de API)
load_dotenv()

# Cargar todos los PDFs de la carpeta especificada usando un loader multihilo
loader = DirectoryLoader(
    os.path.abspath("/Users/juliocolomer/Documents/000-BOOTCAMP-LLM-APPS/003-NOTEBOOKS/005-RAG-IN-DEPTH/003-RAG-PDFS/167-part4/167-part4/pdf-documents"),
    glob="**/*.pdf",
    use_multithreading=True,
    show_progress=True,
    max_concurrency=50,
    loader_cls=UnstructuredPDFLoader,
)
docs = loader.load()

# Inicializar embeddings de OpenAI
embeddings = OpenAIEmbeddings(model='text-embedding-ada-002', )

# Dividir los documentos en chunks semánticos usando SemanticChunker
text_splitter = SemanticChunker(
    embeddings=embeddings
)

# Aplanar la lista de documentos cargados
flattened_docs = [doc[0] for doc in docs if doc]
chunks = text_splitter.split_documents(flattened_docs)

# Indexar los chunks en PGVector (PostgreSQL)
PGVector.from_documents(
    documents=chunks,
    embedding=embeddings,
    collection_name="collection164",
    connection_string="postgresql+psycopg://postgres@localhost:5432/database164",
    pre_delete_collection=True,
)