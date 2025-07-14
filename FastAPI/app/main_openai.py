# Importamos FastAPI para crear la API
from fastapi import FastAPI
# Importamos el middleware CORS para permitir peticiones desde cualquier origen
from fastapi.middleware.cors import CORSMiddleware
# Importamos utilidades de LangChain para OpenAI y plantillas
from langchain import OpenAI, PromptTemplate
from langchain.chains import LLMChain

# Inicializamos la aplicación FastAPI
app = FastAPI()
# Permitimos CORS para todos los orígenes, métodos y cabeceras
app.add_middleware(
    CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'],
)

# Inicializamos el modelo OpenAI de LangChain
langchain_llm = OpenAI(temperature=0)

# Definimos la plantilla de prompt para resumir texto
summarize_template_string = """
        Provide a summary for the following text:
        {text}
"""

# Creamos el objeto PromptTemplate con la plantilla definida
summarize_prompt = PromptTemplate(
    template=summarize_template_string,
    input_variables=['text'],
)

# Creamos la cadena LLMChain que une el modelo y el prompt
summarize_chain = LLMChain(
    llm=langchain_llm,
    prompt=summarize_prompt,
)

# Definimos el endpoint POST para resumir texto
@app.post('/summarize-text')
async def summarize_text(text: str):
    # Ejecutamos la cadena para obtener el resumen
    summary = summarize_chain.run(text=text)
    return {'summary': summary}

