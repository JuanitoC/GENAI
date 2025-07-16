// todo.js
// Componente para renderizar una tarea individual con opciones de edición, completado, generación de poema y borrado

import Image from 'next/image'
import styles from '../styles/todo.module.css'
import { useState } from 'react'

export default function ToDo(props) {
  // Recibe la tarea y los handlers para cambio y borrado
  const { todo, onChange, onDelete } = props;
  // Estado para el poema generado
  const [poem, setPoem] = useState(null); // Guarda el poema generado
  const [isPoemVisible, setIsPoemVisible] = useState(false); // Controla la visibilidad del poema

  // Función para generar un poema usando el backend (LangChain)
  async function generatePoem(id) {
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/todos/write-poem/${id}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });
  
    if (res.ok) {
        const data = await res.json();
        setPoem(data.poem);
        setIsPoemVisible(true); // Muestra el poema cuando se genera
    }
  }

  // Función para cerrar el cuadro del poema
  function closePoemBox() {
    setIsPoemVisible(false);
  }

  // Renderizado del componente
  return (
    <div className={styles.toDoRow} key={todo.id}>
      {/* Checkbox para marcar como completada */}
      <input
        className={styles.toDoCheckbox}
        name="completed"
        type="checkbox"
        checked={todo.completed}
        value={todo.completed}
        onChange={(e) => onChange(e, todo.id)}
      ></input>
      {/* Campo editable para el nombre de la tarea */}
      <input
        className={styles.todoInput}
        autoComplete='off'
        name="name"
        type="text"
        value={todo.name}
        onChange={(e) => onChange(e, todo.id)}
      ></input>
      {/* Botón para generar un poema usando LangChain */}
      <button
        className={styles.generatePoemBtn}
        onClick={() => generatePoem(todo.id)}
      >
        Generate Poem
      </button>
      {/* Botón para eliminar la tarea */}
      <button className={styles.deleteBtn} onClick={() => onDelete(todo.id)}>
        <Image src="/delete-outline.svg" width="24" height="24" />
      </button>
      {/* Cuadro para mostrar el poema generado */}
      {isPoemVisible && (
        <div className={styles.poemBox}>
          <button className={styles.closeButton} onClick={closePoemBox}>
            &times; {/* Icono de cerrar */}
          </button>
          <div className={styles.poem}>
            <p>{poem}</p>
          </div>
        </div>
      )}
    </div>
  );  

}