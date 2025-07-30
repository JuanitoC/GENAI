// Importa los estilos CSS para la lista de tareas
import styles from '../styles/todo-list.module.css'
// Importa hooks de React y utilidades
import { useState, useEffect, useCallback, useRef } from 'react'
import { debounce } from 'lodash'
// Importa el componente ToDo para renderizar cada tarea
import ToDo from './todo'

// Componente principal de la lista de tareas
export default function ToDoList() {
  // Estado para almacenar las tareas
  const [todos, setTodos] = useState(null)
  // Estado para el valor del input principal
  const [mainInput, setMainInput] = useState('')
  // Estado para el filtro de tareas (todas, activas, completadas)
  const [filter, setFilter] = useState()
  // Referencia para evitar múltiples fetchs iniciales
  const didFetchRef = useRef(false)
  
  // useEffect para cargar las tareas solo una vez al montar el componente
  useEffect(() => {
    if (didFetchRef.current === false) {
      didFetchRef.current = true
      fetchTodos()
    }
  }, [])

  // Función para obtener las tareas desde la API, opcionalmente filtrando por completadas
  async function fetchTodos(completed) {
    let path = '/todos'
    if (completed !== undefined) {
      path = `/todos?completed=${completed}`
    }
    const res = await fetch(process.env.NEXT_PUBLIC_API_URL + path)
    const json = await res.json()
    setTodos(json)
  }

  // Crea una versión debounced de updateTodo para evitar múltiples llamadas rápidas
  const debouncedUpdateTodo = useCallback(debounce(updateTodo, 500), [])

  // Maneja los cambios en los campos de cada tarea (checkbox o texto)
  function handleToDoChange(e, id) {
    const target = e.target
    const value = target.type === 'checkbox' ? target.checked : target.value
    const name = target.name
    // Copia el array de tareas
    const copy = [...todos]
    // Busca el índice de la tarea modificada
    const idx = todos.findIndex((todo) => todo.id === id)
    // Crea una nueva tarea con el cambio aplicado
    const changedToDo = {
      ...todos[idx],
      [name]: value
    }
    copy[idx] = changedToDo
    // Actualiza la tarea en el backend (debounced)
    debouncedUpdateTodo(changedToDo)
    // Actualiza el estado local
    setTodos(copy)
  }

  // Actualiza una tarea en el backend
  async function updateTodo(todo) {
    const data = {
      name: todo.name,
      completed: todo.completed
    }
    const res = await fetch(process.env.NEXT_PUBLIC_API_URL + `/todos/${todo.id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
      headers: {
        'Content-Type': 'application/json'
      }
    })
  }

  // Agrega una nueva tarea a la lista y al backend
  async function addToDo(name) {
    const res = await fetch(process.env.NEXT_PUBLIC_API_URL + `/todos/`, {
      method: 'POST',
      body: JSON.stringify({
        name: name,
        completed: false
      }),
      headers: {
        'Content-Type': 'application/json'
      }
    })
    if (res.ok) {
      const json = await res.json();
      const copy = [...todos, json]
      setTodos(copy)
    }
  }

  // Elimina una tarea del backend y del estado local
  async function handleDeleteToDo(id) {
    const res = await fetch(process.env.NEXT_PUBLIC_API_URL + `/todos/${id}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json'
      }
    })
    if (res.ok) {
      const idx = todos.findIndex((todo) => todo.id === id)
      const copy = [...todos]
      copy.splice(idx, 1)
      setTodos(copy)
    }
  }

  // Maneja el cambio de valor en el input principal
  function handleMainInputChange(e) {
    setMainInput(e.target.value)
  }

  // Maneja el evento de presionar una tecla en el input principal
  function handleKeyDown(e) {
    if (e.key === 'Enter') {
      if (mainInput.length > 0) {
        addToDo(mainInput)
        setMainInput('')
      }
    }
  }

  // Cambia el filtro de tareas y recarga la lista según el filtro
  function handleFilterChange(value) {
    setFilter(value)
    fetchTodos(value)
  }

  // Renderizado del componente
  return (
    <div className={styles.container}>
      {/* Input principal para agregar tareas */}
      <div className={styles.mainInputContainer}>
        <input className={styles.mainInput} placeholder="What needs to be done?" value={mainInput} onChange={(e) => handleMainInputChange(e)} onKeyDown={handleKeyDown}></input>
      </div>
      {/* Mensaje de carga mientras se obtienen las tareas */}
      {!todos && (
        <div>Loading...</div>
      )}
      {/* Renderiza la lista de tareas */}
      {todos && (
        <div>
          {todos.map((todo) => {
            return (
              <ToDo key={todo.id} todo={todo} onDelete={handleDeleteToDo} onChange={handleToDoChange} />
            )
          })}
        </div>
      )}
      {/* Botones de filtro para mostrar todas, activas o completadas */}
      <div className={styles.filters}>
        <button className={`${styles.filterBtn} ${filter === undefined && styles.filterActive}`} onClick={() => handleFilterChange()}>All</button>
        <button className={`${styles.filterBtn} ${filter === false && styles.filterActive}`} onClick={() => handleFilterChange(false)}>Active</button>
        <button className={`${styles.filterBtn} ${filter === true && styles.filterActive}`} onClick={() => handleFilterChange(true)}>Completed</button>
      </div>
    </div>
  )
}