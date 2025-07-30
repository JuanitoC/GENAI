"""
Este código crea una API para traducir texto usando un modelo de OpenAI (GPT-3.5-turbo). El flujo es:

1.- Recibe un texto y un idioma destino.
2.- Genera un prompt con esa información.
3.- Llama al modelo de OpenAI con el prompt.
4.- Devuelve la traducción como respuesta.

Puedes probarlo una vez que el servidor está corriendo, enviando peticiones POST a http://localhost:8000/chain con un cuerpo JSON como:

json
Copiar
Editar
{
  "input": {
    "text": "Hello, how are you?",
    "language": "Spanish"
  }
}


add_routes() se encarga automáticamente de exponer el objeto chain como una API REST, siguiendo ciertas convenciones.

🛣 Rutas que expone add_routes
Cuando usas add_routes(app, chain, path="/chain"), se exponen estas rutas automáticamente:

Método HTTP	Ruta	Propósito
POST	/chain/invoke	🔥 Ejecuta el chain
GET	/chain	Documentación de la cadena
GET	/chain/openapi.json	Esquema OpenAPI de la cadena

Así que la ruta que realmente ejecuta el modelo es /chain/invoke y usa el método POST.

"""



# Importa FastAPI, el framework para crear APIs web rápidas y ligeras en Python.
from fastapi import FastAPI

# Importa la función para agregar rutas LangChain a una app FastAPI.
from langserve import add_routes

# Importa una clase para crear plantillas de prompts para modelos de lenguaje.
from langchain_core.prompts import ChatPromptTemplate

# Importa un parser que convierte la salida del modelo en un string.
from langchain_core.output_parsers import StrOutputParser

# Importa la clase de modelo de lenguaje de OpenAI (GPT).
from langchain_openai import ChatOpenAI

# Utilidades para cargar variables de entorno desde un archivo `.env`.
from dotenv import load_dotenv, find_dotenv

import os

# Carga las variables de entorno desde un archivo `.env`, si existe.
_ = load_dotenv(find_dotenv())

# Obtiene la clave de API de OpenAI desde las variables de entorno.
openai_api_key = os.environ["OPENAI_API_KEY"]

# Instancia el modelo GPT-3.5-turbo desde LangChain/OpenAI.
llm = ChatOpenAI(model="gpt-3.5-turbo")

# Crea un parser que convierte la salida del modelo en texto plano.
parser = StrOutputParser()

# Define el mensaje de sistema que se usará como prompt base para el modelo.
system_template = "Translate the following into {language}:"

# Crea una plantilla de conversación tipo "chat" con dos partes:
# 1. Mensaje del sistema que da instrucciones.
# 2. Mensaje del usuario que contiene el texto a traducir.
prompt_template = ChatPromptTemplate.from_messages([
    ('system', system_template),
    ('user', '{text}')
])

# Encadena los pasos: plantilla de prompt -> modelo de lenguaje -> parser de salida
# Esto define la cadena completa de procesamiento para la traducción.
chain = prompt_template | llm | parser

# Crea una instancia de la aplicación FastAPI con metadatos.
app = FastAPI(
  title="simpleTranslator",
  version="1.0",
  description="A simple API server using LangChain's Runnable interfaces",
)

# Agrega una ruta `/chain` a la aplicación FastAPI, la cual expone la `chain` como endpoint.
add_routes(
    app,
    chain,
    path="/chain",
)

# Si se ejecuta el archivo directamente, lanza el servidor con Uvicorn en localhost:8000
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)