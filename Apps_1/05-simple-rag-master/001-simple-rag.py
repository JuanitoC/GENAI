"""
Aplicación simple de RAG (Retrieval-Augmented Generation) sobre un archivo de texto usando LangChain y OpenAI.

Descripción general:
Este script carga un archivo de texto, lo divide en fragmentos, genera embeddings y construye una base de datos vectorial (Chroma) para recuperación semántica. Permite hacer preguntas sobre el contenido del texto utilizando un modelo de lenguaje (LLM) de OpenAI, recuperando los fragmentos más relevantes y generando una respuesta concisa basada en ellos.
"""



import os
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())
openai_api_key = os.environ["OPENAI_API_KEY"]


os.environ["LANGCHAIN_PROJECT"] = "RAGMASTER"

from langchain_openai import ChatOpenAI

# Inicializa el modelo de lenguaje de OpenAI
llm = ChatOpenAI(model="gpt-3.5-turbo")

import bs4
#from langchain import hub
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import HumanMessagePromptTemplate
from langchain_core.prompts import PromptTemplate

# Carga el archivo de texto a analizar
loader = TextLoader("C:/Users/Juan/Desktop/GEN AI/GENAI/Apps 1/05-simple-rag-master/data/be-good.txt")

# Convierte el archivo en documentos
docs = loader.load()

# Divide el texto en fragmentos manejables
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

splits = text_splitter.split_documents(docs)

# Crea una base de datos vectorial (Chroma) a partir de los fragmentos y sus embeddings
vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())

# Obtiene un recuperador semántico a partir del vectorstore
retriever = vectorstore.as_retriever()

# La siguiente línea no es compatible con python 3.11.4
# Para instalar langchain-hub, deberás usar python 3.12.2 o superior
#prompt = hub.pull("rlm/rag-prompt")

# Para seguir usando python 3.11.4, pegamos el prompt desde el hub
prompt  = ChatPromptTemplate(input_variables=['context', 'question'], metadata={'lc_hub_owner': 'rlm', 'lc_hub_repo': 'rag-prompt', 'lc_hub_commit_hash': '50442af133e61576e74536c6556cefe1fac147cad032f4377b60c436e6cdcb6e'}, messages=[HumanMessagePromptTemplate(prompt=PromptTemplate(input_variables=['context', 'question'], template="You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.\nQuestion: {question} \nContext: {context} \nAnswer:"))])

def format_docs(docs):
    """Une el contenido de los documentos recuperados en un solo string."""
    return "\n\n".join(doc.page_content for doc in docs)

# Define la cadena RAG: recupera contexto relevante y genera la respuesta
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# Realiza una pregunta sobre el texto
response = rag_chain.invoke("What is this article about?")

print("\n----------\n")
print("What is this article about?")
print("\n----------\n")
print(response)
print("\n----------\n")