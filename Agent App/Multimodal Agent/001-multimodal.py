import os
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())
openai_api_key = os.environ["OPENAI_API_KEY"]
os.environ["LANGCHAIN_PROJECT"] = "multimodal"

from langchain_openai import ChatOpenAI

chain_gpt_35 = ChatOpenAI(model="gpt-3.5-turbo", max_tokens=1024)
chain_gpt_4_vision = ChatOpenAI(model="gpt-4o", max_tokens=1024)

from typing import Any
import os
from unstructured.partition.pdf import partition_pdf
import pytesseract
import os

# Configura la ruta de tesseract.exe (asegúrate de que la ruta sea correcta en tu sistema)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

input_path = os.getcwd()
output_path = os.path.join(os.getcwd(), "figures")

# Extrae los elementos del PDF: texto, tablas e imágenes
raw_pdf_elements = partition_pdf(
    filename=os.path.join(input_path, "startupai-financial-report-v2.pdf"),
    extract_images_in_pdf=True,
    infer_table_structure=True,
    chunking_strategy="by_title",
    max_characters=4000,
    new_after_n_chars=3800,
    combine_text_under_n_chars=2000,
    image_output_dir_path=output_path,
)

import base64

text_elements = []
table_elements = []
image_elements = []

# Función para codificar imágenes en base64
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Paso 1: Clasifica los elementos extraídos en texto y tablas
for element in raw_pdf_elements:
    # Los elementos de texto contienen 'CompositeElement' en su tipo
    if 'CompositeElement' in str(type(element)):
        text_elements.append(element)
    # Los elementos de tabla contienen 'Table' en su tipo
    elif 'Table' in str(type(element)):
        table_elements.append(element)

# Paso 2: Extrae solo el texto de los elementos, descartando las clases originales
table_elements = [i.text for i in table_elements]
text_elements = [i.text for i in text_elements]

# Imprime la cantidad de tablas encontradas
print("\n----------\n")
print("Cantidad de elementos tipo tabla en el archivo PDF:")
print("\n----------\n")
print(len(table_elements))
print("\n----------\n")

# Imprime la cantidad de textos encontrados
print("\n----------\n")
print("Cantidad de elementos tipo texto en el archivo PDF:")
print("\n----------\n")
print(len(text_elements))
print("\n----------\n")

# Procesa las imágenes extraídas y las codifica en base64
for image_file in os.listdir(output_path):
    if image_file.endswith((".png", ".jpg", ".jpeg")):
        image_path = os.path.join(output_path, image_file)
        encoded_image = encode_image(image_path)
        image_elements.append(encoded_image)

# Imprime la cantidad de imágenes encontradas
print("\n----------\n")
print("Cantidad de elementos tipo imagen en el archivo PDF:")
print("\n----------\n")
print(len(image_elements))
print("\n----------\n")

from langchain.schema.messages import HumanMessage, AIMessage

# Función para resumir textos usando el modelo de lenguaje
def summarize_text(text_element):
    prompt = f"Resume el siguiente texto:\n\n{text_element}\n\nResumen:"
    response = chain_gpt_35.invoke([HumanMessage(content=prompt)])
    return response.content

# Función para resumir tablas usando el modelo de lenguaje
def summarize_table(table_element):
    prompt = f"Resume la siguiente tabla:\n\n{table_element}\n\nResumen:"
    response = chain_gpt_35.invoke([HumanMessage(content=prompt)])
    return response.content

# Función para resumir imágenes usando GPT-4o (multimodal)
def summarize_image(encoded_image):
    prompt = [
        AIMessage(content="Eres un asistente experto en analizar imágenes."),
        HumanMessage(content=[
            {
                "type": "text",
                "text": "Describe el contenido de esta imagen."
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{encoded_image}"
                },
            },
        ])
    ]
    response = chain_gpt_4_vision.invoke(prompt)
    return response.content

# Procesa los elementos de texto (solo los dos primeros para evitar sobrecarga)
text_summaries = []
for i, te in enumerate(text_elements[0:2]):
    summary = summarize_text(te)
    text_summaries.append(summary)
    print(f"{i + 1}º elemento de texto procesado.")
    
# Procesa los elementos de tabla (solo el primero)
table_summaries = []
for i, te in enumerate(table_elements[0:1]):
    summary = summarize_table(te)
    table_summaries.append(summary)
    print(f"{i + 1}º elemento de tabla procesado.")
    
# Procesa los elementos de imagen (hasta 8 imágenes)
image_summaries = []
for i, ie in enumerate(image_elements[0:8]):
    summary = summarize_image(ie)
    image_summaries.append(summary)
    print(f"{i + 1}º elemento de imagen procesado.")
    
import uuid

from langchain_openai import OpenAIEmbeddings
from langchain.retrievers.multi_vector import MultiVectorRetriever
from langchain.schema.document import Document
from langchain.storage import InMemoryStore
from langchain_chroma import Chroma

# Inicializa la base de datos vectorial Chroma y el almacén de documentos en memoria
vectorstorev2 = Chroma(collection_name="summaries", embedding_function=OpenAIEmbeddings())
storev2 = InMemoryStore()
id_key = "doc_id"

# Inicializa el recuperador multi-vector
dretrieverv2 = MultiVectorRetriever(vectorstore=vectorstorev2, docstore=storev2, id_key=id_key)

# Función para agregar documentos (resúmenes y originales) al recuperador multi-vector
def add_documents_to_retriever(summaries, original_contents):
    doc_ids = [str(uuid.uuid4()) for _ in summaries]
    summary_docs = [
        Document(page_content=s, metadata={id_key: doc_ids[i]})
        for i, s in enumerate(summaries)
    ]
    retrieverv2.vectorstore.add_documents(summary_docs)
    retrieverv2.docstore.mset(list(zip(doc_ids, original_contents)))
    
# Agrega los resúmenes de texto
add_documents_to_retriever(text_summaries, text_elements)

# Agrega los resúmenes de tablas
add_documents_to_retriever(table_summaries, table_elements)

# Agrega los resúmenes de imágenes (solo los resúmenes, no las imágenes crudas)
add_documents_to_retriever(image_summaries, image_summaries)

print("\n----------\n")
print("¿Qué ves en las imágenes?")
print("\n----------\n")
print(retrieverv2.invoke(
    "¿Qué ves en las imágenes?"
))
print("\n----------\n")

from langchain.schema.runnable import RunnablePassthrough
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser

# Plantilla de prompt para el modelo conversacional
template = """Responde la pregunta basándote únicamente en el siguiente contexto, que puede incluir texto, imágenes y tablas:\n{context}\nPregunta: {question}\n"""
prompt = ChatPromptTemplate.from_template(template)

model = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")

# Cadena de procesamiento para preguntas y respuestas con contexto recuperado
chain = (
    {"context": retrieverv2, "question": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)

print("\n----------\n")
print("¿Qué ves en las imágenes de la base de datos?")
print("\n----------\n")
print(chain.invoke(
     "¿Qué ves en las imágenes de la base de datos?"
))
print("\n----------\n")
print("¿Cuál es el nombre de la empresa?")
print("\n----------\n")
print(chain.invoke(
     "¿Cuál es el nombre de la empresa?"
))
print("\n----------\n")
print("¿Qué producto aparece en la imagen?")
print("\n----------\n")
print(chain.invoke(
     "¿Qué producto aparece en la imagen?"
))
print("\n----------\n")
print("¿Cuáles son los gastos totales de la empresa?")
print("\n----------\n")
print(chain.invoke(
     "¿Cuáles son los gastos totales de la empresa?"
))
print("\n----------\n")
print("¿Cuál es el ROI?")
print("\n----------\n")
print(chain.invoke(
     "¿Cuál es el ROI?"
))
print("\n----------\n")
print("¿Cuánto vendió la empresa en 2023?")
print("\n----------\n")
print(chain.invoke(
     "¿Cuánto vendió la empresa en 2023?"
))
print("\n----------\n")
print("¿Y en 2022?")
print("\n----------\n")
print(chain.invoke(
     "¿Y en 2022?"
))