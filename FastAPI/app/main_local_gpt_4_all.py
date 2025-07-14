# Importamos FastAPI para crear la API
from fastapi import FastAPI
# Importamos el middleware CORS para permitir peticiones desde cualquier origen
from fastapi.middleware.cors import CORSMiddleware
# Importamos utilidades de LangChain para plantillas y cadenas LLM
from langchain import PromptTemplate
from langchain.chains import LLMChain
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.llms import GPT4All

# Inicializamos la aplicación FastAPI
app = FastAPI()
# Permitimos CORS para todos los orígenes, métodos y cabeceras
app.add_middleware(
    CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'],
)

# Definimos la ruta del modelo local de GPT4All
# y configuramos los callbacks para mostrar la salida en consola
# Cargamos el modelo local de lenguaje
gpt4_all_model_path = "./ggml-gpt4all-j-v1.3-groovy.bin"
callbacks = [StreamingStdOutCallbackHandler()]
local_llm = GPT4All(model=gpt4_all_model_path, callbacks=callbacks, verbose=True)

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
