"""
Aplicación de extracción de datos clave de texto usando LangChain y OpenAI.

Descripción general:
Esta aplicación utiliza un modelo de lenguaje (LLM) para extraer información estructurada sobre personas a partir de comentarios o textos. Define esquemas de datos con Pydantic, crea prompts personalizados y utiliza cadenas de procesamiento para obtener entidades como nombre, apellido y país de personas mencionadas en el texto.
"""

import os
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())
openai_api_key = os.environ["OPENAI_API_KEY"]

from langchain_openai import ChatOpenAI

# Inicializa el modelo de lenguaje de OpenAI
llm = ChatOpenAI(model="gpt-3.5-turbo-0125")

from typing import Optional, List
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Definición del esquema de persona para la extracción
class Person(BaseModel):
    """Información sobre una persona."""
    # Cada campo es opcional y tiene una descripción para mejorar la extracción
    name: Optional[str] = Field(default=None, description="The name of the person")
    lastname: Optional[str] = Field(
        default=None, description="The lastname of the person if known"
    )
    country: Optional[str] = Field(
        default=None, description="The country of the person if known"
    )

# Definición del esquema para extraer múltiples personas
class Data(BaseModel):
    """Datos extraídos sobre personas."""
    people: List[Person]

# Define un prompt personalizado para dar instrucciones al modelo
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert extraction algorithm. "
            "Only extract relevant information from the text. "
            "If you do not know the value of an attribute asked to extract, "
            "return null for the attribute's value.",
        ),
        ("human", "{text}"),
    ]
)

# Crea la cadena de procesamiento para extraer una sola persona
chain_single = prompt | llm.with_structured_output(schema=Person)

# Ejemplo de comentario para extraer una sola persona
comment = "I absolutely love this product! It's been a game-changer for my daily routine. The quality is top-notch and the customer service is outstanding. I've recommended it to all my friends and family. - Sarah Johnson, USA"

response = chain_single.invoke({"text": comment})

print("\n----------\n")
print("Key data extraction:")
print("\n----------\n")
print(response)
print("\n----------\n")

# Crea la cadena de procesamiento para extraer una lista de personas
chain = prompt | llm.with_structured_output(schema=Data)

# Ejemplo de comentario para extraer una lista de personas
comment = "I'm so impressed with this product! It has truly transformed how I approach my daily tasks. The quality exceeds my expectations, and the customer support is truly exceptional. I've already suggested it to all my colleagues and relatives. - Emily Clarke, Canada"

response = chain.invoke({"text": comment})

print("\n----------\n")
print("Key data extraction of a list of entities:")
print("\n----------\n")
print(response)
print("\n----------\n")

# Ejemplo de texto que menciona varias personas
text_input = """
Alice Johnson from Canada recently reviewed a book she loved. Meanwhile, Bob Smith from the USA shared his insights on the same book in a different review. Both reviews were very insightful.
"""

# Invoca la cadena de procesamiento sobre el texto con varias personas
response = chain.invoke({"text": text_input})

# Muestra los datos extraídos
print("\n----------\n")
print("Key data extraction of a review with several users:")
print("\n----------\n")
print(response)
print("\n----------\n")
