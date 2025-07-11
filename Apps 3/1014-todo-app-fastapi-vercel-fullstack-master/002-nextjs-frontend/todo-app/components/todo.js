// Importa el componente de imagen optimizada de Next.js
import Image from 'next/image'
// Importa los estilos CSS para el componente de tarea
import styles from '../styles/todo.module.css'

// Componente funcional que representa una sola tarea (ToDo)
export default function ToDo(props) {
  // Desestructura las props: la tarea, el manejador de cambios y el de borrado
  const { todo, onChange, onDelete } = props;
  return (
    <div className={styles.toDoRow} key={todo.id}>
      {/* Checkbox para marcar la tarea como completada o no */}
      <input 
        className={styles.toDoCheckbox} 
        name="completed" 
        type="checkbox" 
        checked={todo.completed} 
        value={todo.completed} 
        onChange={(e) => onChange(e, todo.id)}
      >
      </input>
      {/* Input de texto para editar el nombre de la tarea */}
      <input 
        className={styles.todoInput} 
        autoComplete='off' 
        name="name" 
        type="text" 
        value={todo.name} 
        onChange={(e) => onChange(e, todo.id)}
      >
      </input>
      {/* Botón para eliminar la tarea, muestra un ícono de papelera */}
      <button 
        className={styles.deleteBtn} 
        onClick={() => onDelete(todo.id)}>
        <Image src="/delete-outline.svg" width="24" height="24" />
      </button>
    </div>
  )
}