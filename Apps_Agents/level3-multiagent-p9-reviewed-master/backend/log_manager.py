"""
RESUMEN DEL ARCHIVO:
Este archivo implementa un sistema de gestión de logs y eventos para el sistema multiagente.
Proporciona funcionalidad para:

- Rastrear eventos y estados de las investigaciones multiagente
- Almacenar resultados de manera thread-safe usando locks
- Mantener un historial de eventos con timestamps
- Gestionar el estado de las investigaciones (STARTED, COMPLETE, ERROR)

El sistema utiliza un diccionario global thread-safe para almacenar los outputs
y eventos de cada investigación identificada por un input_id único.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict
from threading import Lock

@dataclass
class Event:
    """
    Clase para representar un evento individual en el sistema de logging.
    
    Atributos:
        timestamp (datetime): Momento exacto cuando ocurrió el evento
        data (str): Descripción o datos del evento
    """
    timestamp: datetime
    data: str


@dataclass
class Output:
    """
    Clase para representar el resultado completo de una investigación multiagente.
    
    Atributos:
        status (str): Estado actual de la investigación ('STARTED', 'COMPLETE', 'ERROR')
        events (List[Event]): Lista cronológica de eventos durante la investigación
        result (str): Resultado final de la investigación (JSON string o mensaje de error)
    """
    status: str
    events: List[Event]
    result: str

# Variables globales para almacenamiento thread-safe de outputs
outputs_lock = Lock()  # Lock para sincronización entre threads
outputs: Dict[str, "Output"] = {}  # Diccionario que mapea input_id -> Output

def append_event(input_id: str, event_data: str):
    """
    Agrega un nuevo evento al historial de una investigación específica.
    
    Esta función es thread-safe y maneja tanto la creación de nuevos outputs
    como la adición de eventos a outputs existentes.
    
    Args:
        input_id (str): Identificador único de la investigación
        event_data (str): Descripción del evento a agregar
    
    Comportamiento:
        - Si el input_id no existe, crea un nuevo Output con status 'STARTED'
        - Si el input_id existe, agrega el evento a la lista existente
        - Utiliza un lock para garantizar thread-safety
    """
    with outputs_lock:
        if input_id not in outputs:
            print(f"Start output {input_id}")
            # Crear nuevo output para esta investigación
            outputs[input_id] = Output(
                status='STARTED',
                events=[],
                result='')
        else:
            print("Appending event for output")
            
        # Agregar el nuevo evento con timestamp actual
        outputs[input_id].events.append(
            Event(timestamp=datetime.now(), data=event_data))