# Este código utiliza un modelo de lenguaje (LLM) para responder preguntas sobre una base de datos SQL.

# 1. Carga la clave de API y configura el modelo de lenguaje de OpenAI.
# 2. Conecta con una base de datos SQLite que contiene información de árboles en San Francisco.
# 3. Genera consultas SQL automáticamente a partir de preguntas en lenguaje natural.
# 4. Ejecuta las consultas y muestra los resultados.
# 5. Utiliza el LLM para generar respuestas finales combinando la pregunta, la consulta y el resultado.

# Importa librerías necesarias para cargar variables de entorno
import os
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())
# Obtiene la clave de API de OpenAI desde las variables de entorno
openai_api_key = os.environ["OPENAI_API_KEY"]

# Importa el modelo de lenguaje de OpenAI a través de LangChain
from langchain_openai import ChatOpenAI

# Inicializa el modelo LLM de OpenAI (GPT-3.5 Turbo)
llm = ChatOpenAI(model="gpt-3.5-turbo-0125")

# Importa la utilidad para trabajar con bases de datos SQL
from langchain_community.utilities import SQLDatabase

# Define la ruta a la base de datos SQLite
sqlite_db_path = "data/street_tree_db.sqlite"

# Crea una instancia de la base de datos SQL
db = SQLDatabase.from_uri(f"sqlite:///{sqlite_db_path}")

# Importa la función para crear cadenas de consulta SQL
from langchain.chains import create_sql_query_chain

# Crea una cadena que genera consultas SQL a partir de preguntas en lenguaje natural
chain = create_sql_query_chain(llm, db)

# Invoca la cadena con una pregunta específica
response = chain.invoke({"question": "List the species of trees that are present in San Francisco"})

print("\n----------\n")

print("List the species of trees that are present in San Francisco")

print("\n----------\n")
print(response)

print("\n----------\n")

print("Query executed:")

print("\n----------\n")

# Ejecuta la consulta SQL generada y muestra el resultado
print(db.run(response))

print("\n----------\n")

# Importa la herramienta para ejecutar consultas SQL directamente
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool

# Crea una herramienta para ejecutar consultas SQL
execute_query = QuerySQLDataBaseTool(db=db)

# Vuelve a crear la cadena para generar consultas SQL
write_query = create_sql_query_chain(llm, db)

# Encadena la generación y ejecución de la consulta SQL
chain = write_query | execute_query

# Invoca la cadena completa con la misma pregunta
response = chain.invoke({"question": "List the species of trees that are present in San Francisco"})

print("\n----------\n")

print("List the species of trees that are present in San Francisco (with query execution included)")

print("\n----------\n")
print(response)

print("\n----------\n")

# Importa utilidades para manipular la salida y los prompts
from operator import itemgetter

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough

# Define un prompt para que el LLM genere una respuesta final basada en la pregunta, la consulta SQL y el resultado
answer_prompt = PromptTemplate.from_template(
    """Given the following user question, corresponding SQL query, and SQL result, answer the user question.


Answer: """
)

# Crea una cadena más avanzada que pasa la pregunta, la consulta y el resultado al LLM para obtener una respuesta final
chain = (
    RunnablePassthrough.assign(query=write_query).assign(
        result=itemgetter("query") | execute_query
    )
    | answer_prompt
    | llm
    | StrOutputParser()
)

# Invoca la cadena avanzada con la pregunta original
response = chain.invoke({"question": "List the species of trees that are present in San Francisco"})

print("\n----------\n")

print("List the species of trees that are present in San Francisco (passing question and result to the LLM)")

print("\n----------\n")
print(response)

print("\n----------\n")
