# example_tools_demo.py

from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field


from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
import os

from dotenv import load_dotenv,find_dotenv

_ = load_dotenv(find_dotenv())



# 📌 Tool 1: Herramienta de búsqueda web (Serper)
search_tool = SerperDevTool()


# Tool 2: Contador de palabras



class ContadorPalabrasInput(BaseModel):
    """Input schema for ContadorPalabrasTool."""
    texto: str = Field(..., description="El texto del cual se quieren contar las palabras.")


class ContadorPalabrasTool(BaseTool):
    name: str = "contador_palabras"
    description: str = (
        "Cuenta el número de palabras en un texto dado. Útil para análisis de contenido y estadísticas de texto."
    )
    args_schema: Type[BaseModel] = ContadorPalabrasInput

    def _run(self, texto: str) -> str:
        # Cuenta las palabras en el texto
        palabras = texto.split()
        cantidad = len(palabras)
        
        return f"El texto contiene {cantidad} palabras."

    def _arun(self, texto: str) -> str:
        # Versión asíncrona (requerida por BaseTool)
        return self._run(texto)

# Crear instancia de la herramienta
contador_tool = ContadorPalabrasTool()

# 👨‍🔬 Agente 1: Investiga sobre un tema
researcher = Agent(
    role="Investigador web",
    goal="Buscar información actualizada sobre el cambio climático",
    backstory="Especialista en encontrar información reciente y precisa.",
    tools=[search_tool],
    allow_delegation=False
)

# 🧮 Agente 2: Analiza y cuenta palabras
counter = Agent(
    role="Analista de texto",
    goal="Analizar y contar palabras en el texto investigado",
    backstory="Asistente que analiza texto y ofrece estadísticas básicas.",
    tools=[contador_tool],
    allow_delegation=False
)

# 🧠 Tareas
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

# 👥 Crew
crew = Crew(
    agents=[researcher, counter],
    tasks=[task1, task2],
    process=Process.sequential,
    verbose=True
)

# 🚀 Ejecutar
resultado = crew.kickoff()

# 💾 Guardar resultado final en un archivo
with open("output_crew.txt", "w", encoding="utf-8") as f:
    f.write(resultado.raw)

# 📢 Mostrar resultado en consola
print("\n📝 Resultado Final:")
print(resultado.raw)
