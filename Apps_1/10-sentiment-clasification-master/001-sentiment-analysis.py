"""
🧠 ¿Qué hace este código?
Toma un texto político (pro-Trump o pro-Biden).

Usa un modelo LLM para extraer 3 propiedades estructuradas:

sentiment (estado emocional)

political_tendency (ideología)

language (idioma)

Primero lo hace libremente, y luego con restricciones (enum) para limitar los valores válidos.

Imprime el resultado estructurado para ambos textos.

"""


# Carga variables de entorno desde un archivo .env
import os
from dotenv import load_dotenv, find_dotenv

# Carga la API key desde el entorno
_ = load_dotenv(find_dotenv())
openai_api_key = os.environ["OPENAI_API_KEY"]
os.environ["LANGCHAIN_PROJECT"] = "App 1 - Classifier"

# Importa el modelo de lenguaje desde LangChain con soporte para OpenAI
from langchain_openai import ChatOpenAI

# Instancia del modelo LLM (chat) con un modelo específico de OpenAI
llm = ChatOpenAI(model="gpt-3.5-turbo-0125")

# Importa plantilla para crear prompts y esquema para output estructurado
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field

# Define un prompt para extraer información estructurada de un texto
tagging_prompt = ChatPromptTemplate.from_template(
    """
Extract the desired information from the following passage.

Only extract the properties mentioned in the 'Classification' function.

Passage:
{input}
"""
)

# Define el esquema de salida usando Pydantic
# Este schema dice qué atributos debe identificar el modelo en el texto
class Classification(BaseModel):
    sentiment: str = Field(description="The sentiment of the text")
    political_tendency: str = Field(
        description="The political tendency of the user"
    )
    language: str = Field(description="The language the text is written in")

# Vuelve a crear el modelo LLM con el schema de salida estructurado
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0125").with_structured_output(
    Classification
)

# Crea una cadena que conecta el prompt con el modelo
tagging_chain = tagging_prompt | llm

# Texto simulado de un seguidor de Trump
trump_follower = "I'm confident that President Trump's leadership and track record will once again resonate with Americans. His strong stance on economic growth and national security is exactly what our country needs at this pivotal moment. We need to bring back the proven leadership that can make America great again!"

# Texto simulado de un seguidor de Biden
biden_follower = "I believe President Biden's compassionate and steady approach is vital for our nation right now. His commitment to healthcare reform, climate change, and restoring our international alliances is crucial. It's time to continue the progress and ensure a future that benefits all Americans."

# Ejecuta el modelo con el texto del seguidor de Trump
response = tagging_chain.invoke({"input": trump_follower})

# Imprime los resultados
print("\n----------\n")
print("Sentiment analysis Trump follower:")
print("\n----------\n")
print(response)
print("\n----------\n")

# Ejecuta el modelo con el texto del seguidor de Biden
response = tagging_chain.invoke({"input": biden_follower})

# Imprime los resultados
print("\n----------\n")
print("Sentiment analysis Biden follower:")
print("\n----------\n")
print(response)
print("\n----------\n")

# ------- VERSIÓN CON ENUMS -------

# Se redefine el esquema Classification con valores predefinidos (enum)
class Classification(BaseModel):
    sentiment: str = Field(..., enum=["happy", "neutral", "sad"])
    political_tendency: str = Field(
        ..., description="The political tendency of the user",
        enum=["conservative", "liberal", "independent"]
    )
    language: str = Field(..., enum=["spanish", "english"])

# Se vuelve a crear el prompt (idéntico, pero ahora adaptado al nuevo schema)
tagging_prompt = ChatPromptTemplate.from_template(
    """
Extract the desired information from the following passage.

Only extract the properties mentioned in the 'Classification' function.

Passage:
{input}
"""
)

# Se vuelve a configurar el LLM para trabajar con el nuevo schema (con enums)
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0125").with_structured_output(
    Classification
)

# Se vuelve a crear la cadena que conecta prompt + modelo
tagging_chain = tagging_prompt | llm

# Ejecuta la cadena con el texto de Trump follower, esta vez usando enums
response = tagging_chain.invoke({"input": trump_follower})

print("\n----------\n")
print("Sentiment analysis Trump follower (with a list of options using enums):")
print("\n----------\n")
print(response)
print("\n----------\n")

# Ejecuta la cadena con el texto de Biden follower, usando enums
response = tagging_chain.invoke({"input": biden_follower})

print("\n----------\n")
print("Sentiment analysis Biden follower (with a list of options using enums):")
print("\n----------\n")
print(response)
print("\n----------\n")
