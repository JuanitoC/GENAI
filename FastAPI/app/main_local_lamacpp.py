# Importamos FastAPI para crear la API
from fastapi import FastAPI
# Importamos el middleware CORS para permitir peticiones desde cualquier origen
from fastapi.middleware.cors import CORSMiddleware
# Importamos utilidades de LangChain para LlamaCpp y plantillas
from langchain import LlamaCpp, PromptTemplate
from langchain.chains import LLMChain
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

# Inicializamos la aplicación FastAPI
app = FastAPI()
# Permitimos CORS para todos los orígenes, métodos y cabeceras
app.add_middleware(
    CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'],
)

# Configuramos el callback manager para mostrar la salida en consola
callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
# Cargamos el modelo local LlamaCpp
local_llm = LlamaCpp(
    #model_path="./ggml-vic7b-uncensored-q4_0.bin",
    model_path="awizardLM-7B.ggmlv3.q4_0.bin",
    callback_manager=callback_manager,
    verbose=True
)

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
    llm=local_llm,
    prompt=summarize_prompt,
)

# Definimos el endpoint POST para resumir texto
@app.post('/summarize-text')
async def summarize_text(text: str):
    # Ejecutamos la cadena para obtener el resumen
    summary = summarize_chain.run(text=text)
    return {'summary': summary}
