from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool

import os
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

# Herramientas
search_tool = SerperDevTool()

class ContadorPalabrasInput(BaseModel):
    texto: str = Field(..., json_schema_extra={"description": "El texto del cual se quieren contar las palabras."})

class ContadorPalabrasTool(BaseTool):
    name: str = "contador_palabras"
    description: str = (
        "Cuenta el número de palabras en un texto dado. Útil para análisis de contenido y estadísticas de texto."
    )
    args_schema: Type[BaseModel] = ContadorPalabrasInput

    def _run(self, texto: str) -> str:
        cantidad = len(texto.split())
        return f"El texto contiene {cantidad} palabras."

    def _arun(self, texto: str) -> str:
        return self._run(texto)

contador_tool = ContadorPalabrasTool()

# Agentes
researcher = Agent(
    role="Investigador web",
    goal="Buscar información actualizada sobre el cambio climático",
    backstory="Especialista en encontrar información reciente y precisa.",
    tools=[search_tool],
    allow_delegation=False,
    verbose=True
)

counter = Agent(
    role="Analista de texto",
    goal="Analizar y contar palabras en el texto investigado",
    backstory="Asistente que analiza texto y ofrece estadísticas básicas.",
    tools=[contador_tool],
    allow_delegation=False,
    verbose=True
)

# Tareas
task1 = Task(
    description="Busca información actualizada sobre el cambio climático en 2025.",
    expected_output="Un texto breve con datos recientes del tema.",
    agent=researcher,
    output_file="output_task1.txt"
)

task2 = Task(
    description="Analiza el texto anterior y cuenta cuántas palabras tiene. Responde solo con el número total de palabras.",
    expected_output="Solo responde con el número total de palabras.",
    agent=counter,
    output_file="output_task2.txt"
)

# Callbacks
def my_task_callback(task_output):
    print("\n📌 [TASK CALLBACK]")
    print("🔸 Tipo:", type(task_output).__name__)
    print("🔸 Atributos:", getattr(task_output, "__dict__", {}))

def my_step_callback(step_output):
    print("\n📌 [STEP CALLBACK]")
    print("🔸 Tipo:", type(step_output).__name__)
    print("🔸 Atributos:", getattr(step_output, "__dict__", {}))

# Crew
crew = Crew(
    agents=[researcher, counter],
    tasks=[task1, task2],
    process=Process.sequential,
    verbose=True,
    task_callback=my_task_callback,
    step_callback=my_step_callback,
    output_log_file="crew_execution_log.json"
)

# Ejecución
resultado = crew.kickoff()

# Guardar resultado final
with open("output_crew.txt", "w", encoding="utf-8") as f:
    f.write(resultado.raw)

print("\n📝 Resultado Final:")
print(resultado.raw)
