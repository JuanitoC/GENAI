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

# Definimos la plantilla de prompt para NER y grafo en mermaid.js
ner_and_graph_prompt_string = """
	Your first task is to extract all entities (named entity recognition).
	Secondly, create a mermaid.js graph describing the relationships between these entities.
	{text}
"""

# Creamos el objeto PromptTemplate con la plantilla definida
ner_graph_prompt = PromptTemplate(
    template=ner_and_graph_prompt_string,
    input_variables=['text'],
)

# Creamos la cadena LLMChain que une el modelo y el prompt
ner_graph_chain = LLMChain(
    llm=local_llm,
    prompt=ner_graph_prompt,
)

# Definimos el endpoint POST para extraer entidades y grafo
@app.post('/extract-ner-graph')
async def extract_ner_graph(text: str):
    # Ejecutamos la cadena para obtener el resultado
    output = ner_graph_chain.run(text=text)
    return {'output': output}