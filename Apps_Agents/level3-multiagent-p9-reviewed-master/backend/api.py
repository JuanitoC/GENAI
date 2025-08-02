"""
RESUMEN DEL ARCHIVO:
Este archivo implementa la API REST de Flask que sirve como interfaz para el sistema
multiagente de investigación. Proporciona endpoints para iniciar investigaciones
y consultar el estado de las mismas.

Endpoints principales:
- POST /api/multiagent: Inicia una nueva investigación multiagente
- GET /api/multiagent/<input_id>: Consulta el estado y resultados de una investigación

Características principales:
- API REST con Flask
- CORS habilitado para frontend
- Ejecución asíncrona de investigaciones en threads separados
- Sistema de logging y seguimiento de eventos
- Manejo de errores robusto
- Respuestas JSON estructuradas

La API actúa como la capa de presentación del sistema multiagente,
permitiendo a los clientes iniciar investigaciones y consultar resultados
de manera asíncrona.
"""

from flask import Flask, jsonify, request, abort
from uuid import uuid4
from threading import Thread
from crews import TechnologyResearchCrew
from log_manager import append_event, outputs, outputs_lock, Event
from datetime import datetime
import json
from flask_cors import CORS

# Configuración de la aplicación Flask
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})  # Habilitar CORS para todos los orígenes

def kickoff_crew(input_id, technologies: list[str], businessareas: list[str]):
    """
    Función que ejecuta la crew de investigación en un thread separado.
    
    Esta función se ejecuta de manera asíncrona para no bloquear la API
    mientras se realiza la investigación. Es responsable de:
    - Crear y configurar la crew de investigación
    - Ejecutar la investigación completa
    - Manejar errores y actualizar el estado
    - Registrar eventos en el sistema de logging
    
    Args:
        input_id (str): Identificador único de la investigación
        technologies (list[str]): Lista de tecnologías a investigar
        businessareas (list[str]): Lista de áreas de negocio a investigar
        
    Comportamiento:
        - Crea una nueva instancia de TechnologyResearchCrew
        - Configura la crew con las tecnologías y áreas de negocio
        - Ejecuta la investigación
        - Actualiza el estado en el sistema de logging
        - Maneja errores y los registra apropiadamente
    """
    print(f"Running crew for {input_id} with technologies {technologies} and businessareas {businessareas}")

    results = None
    try:
        # Crear y configurar la crew de investigación
        company_research_crew = TechnologyResearchCrew(input_id)
        company_research_crew.setup_crew(
            technologies, businessareas)
        # Ejecutar la investigación
        results = company_research_crew.kickoff()

    except Exception as e:
        # Manejar errores y registrarlos
        print(f"CREW FAILED: {str(e)}")
        append_event(input_id, f"CREW FAILED: {str(e)}")
        with outputs_lock:
            outputs[input_id].status = 'ERROR'
            outputs[input_id].result = str(e)

    # Actualizar estado final de la investigación
    with outputs_lock:
        outputs[input_id].status = 'COMPLETE'
        outputs[input_id].result = results
        outputs[input_id].events.append(
            Event(timestamp=datetime.now(), data="Crew complete"))

@app.route('/api/multiagent', methods=['POST'])
def run_crew():
    """
    Endpoint para iniciar una nueva investigación multiagente.
    
    Este endpoint recibe una solicitud POST con las tecnologías y áreas de negocio
    a investigar, genera un ID único para la investigación, y la ejecuta de manera
    asíncrona en un thread separado.
    
    Request Body (JSON):
        {
            "technologies": ["AI", "Blockchain", ...],
            "businessareas": ["Healthcare", "Finance", ...]
        }
        
    Returns:
        JSON con el input_id generado para rastrear la investigación
        
    Status Codes:
        - 200: Investigación iniciada exitosamente
        - 400: Datos de entrada inválidos o incompletos
    """
    data = request.json
    # Validar que los datos requeridos estén presentes
    if not data or 'technologies' not in data or 'businessareas' not in data:
        abort(400, description="Invalid request with missing data.")
 
    # Generar ID único para esta investigación
    input_id = str(uuid4())
    technologies = data['technologies']
    businessareas = data['businessareas']
    
    # Ejecutar la investigación en un thread separado para no bloquear la API
    thread = Thread(target=kickoff_crew, args=(input_id, technologies, businessareas))
    thread.start()
    
    # Retornar el input_id para que el cliente pueda rastrear el progreso
    return jsonify({"input_id": input_id}), 200


@app.route('/api/multiagent/<input_id>', methods=['GET'])
def get_status(input_id):
    """
    Endpoint para consultar el estado y resultados de una investigación.
    
    Este endpoint permite a los clientes consultar el progreso de una investigación
    específica, incluyendo su estado actual, resultados finales y historial de eventos.
    
    Args:
        input_id (str): Identificador único de la investigación
        
    Returns:
        JSON con el estado, resultados y eventos de la investigación
        
    Status Codes:
        - 200: Información recuperada exitosamente
        - 404: Investigación no encontrada
        
    Response Structure:
        {
            "input_id": "uuid",
            "status": "STARTED|COMPLETE|ERROR",
            "result": {...},  // JSON parseado o string
            "events": [{"timestamp": "...", "data": "..."}]
        }
    """
    with outputs_lock:
        output = outputs.get(input_id)
        if output is None:
            abort(404, description="Output not found")

     # Intentar parsear el resultado como JSON para mejor estructuración
    try:
        result_json = json.loads(output.result)
    except json.JSONDecodeError:
        # Si el parsing falla, usar el resultado original como string
        result_json = output.result

    # Retornar información completa de la investigación
    return jsonify({
        "input_id": input_id,
        "status": output.status,
        "result": result_json,
        "events": [{"timestamp": event.timestamp.isoformat(), "data": event.data} for event in output.events]
    })

if __name__ == '__main__':
    # Ejecutar la aplicación Flask en modo debug en el puerto 3001
    app.run(debug=True, port=3001)