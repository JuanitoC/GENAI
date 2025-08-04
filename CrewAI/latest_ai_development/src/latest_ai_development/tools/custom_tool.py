from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field


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
