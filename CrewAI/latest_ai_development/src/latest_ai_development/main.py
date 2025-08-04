#!/usr/bin/env python
"""
RESUMEN:
Este archivo es el punto de entrada principal para ejecutar el crew de desarrollo de IA más reciente.
Proporciona funciones para ejecutar, entrenar, reproducir y probar el crew de manera local.
El crew se enfoca en analizar y desarrollar contenido relacionado con el desarrollo más reciente de IA LLMs.
"""

import sys
import warnings
import dotenv
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

from datetime import datetime

from crew import LatestAiDevelopment

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# Este archivo principal está destinado a ser una forma de ejecutar tu
# crew localmente, así que abstente de agregar lógica innecesaria en este archivo.
# Reemplaza con las entradas que quieres probar, automáticamente
# interpolará cualquier información de tareas y agentes

def run():
    """
    Ejecuta el crew.
    """
    inputs = {
        'topic': 'AI LLMs',
        'current_year': str(datetime.now().year)
    }
    
    try:
        LatestAiDevelopment().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"Ocurrió un error mientras se ejecutaba el crew: {e}")


def train():
    """
    Entrena el crew para un número dado de iteraciones.
    """
    inputs = {
        "topic": "AI LLMs",
        'current_year': str(datetime.now().year)
    }
    try:
        LatestAiDevelopment().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"Ocurrió un error mientras se entrenaba el crew: {e}")

def replay():
    """
    Reproduce la ejecución del crew desde una tarea específica.
    """
    try:
        LatestAiDevelopment().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"Ocurrió un error mientras se reproducía el crew: {e}")

def test():
    """
    Prueba la ejecución del crew y devuelve los resultados.
    """
    inputs = {
        "topic": "AI LLMs",
        "current_year": str(datetime.now().year)
    }
    
    try:
        LatestAiDevelopment().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"Ocurrió un error mientras se probaba el crew: {e}")


if __name__ == "__main__":
    run()