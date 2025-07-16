// todo-list.js
// Componente principal para mostrar, filtrar, crear, editar y eliminar tareas (ToDo)

import styles from '../styles/todo-list.module.css'
import { useState, useEffect, useCallback, useRef } from 'react'
import { debounce } from 'lodash'
import ToDo from './todo'

export default function ToDoList() {
  // Estado para la lista de tareas
  const [todos, setTodos] = useState(null)
  // Estado para el input principal
  const [mainInput, setMainInput] = useState('')
  // Estado para el filtro de tareas
  const [filter, setFilter] = useState()
  // Referencia para evitar múltiples fetchs
  const didFetchRef = useRef(false)
  
  // Cargar las tareas al montar el componente
  useEffect(() => {
    if (didFetchRef.current === false) {
      didFetchRef.current = true
      fetchTodos()
    }
  }, [])

  // Función para obtener las tareas desde el backend, opcionalmente filtrando por 'completed'
  async function fetchTodos(completed) {
    let path = '/todos'
    if (completed !== undefined) {
      path = `/todos?completed=${completed}`
    }
    const res = await fetch(process.env.NEXT_PUBLIC_API_URL + path)
    const json = await res.json()
    setTodos(json)
  }

  // Actualización de tarea con debounce para evitar llamadas excesivas
  const debouncedUpdateTodo = useCallback(debounce(updateTodo, 500), [])

  // Maneja el cambio de campos en una tarea (checkbox o texto)
  function handleToDoChange(e, id) {
    const target = e.target
    const value = target.type === 'checkbox' ? target.checked : target.value
    const name = target.name
    const copy = [...todos]
    const idx = todos.findIndex((todo) => todo.id === id)
    const changedToDo = {
      ...todos[idx],
      [name]: value
    }
    copy[idx] = changedToDo
    debouncedUpdateTodo(changedToDo)
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

  // Crea una nueva tarea en el backend
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

  // Elimina una tarea por su ID
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
  
  // Maneja el cambio en el input principal
  function handleMainInputChange(e) {
    setMainInput(e.target.value)
  }

  // Maneja el evento Enter para crear una nueva tarea
  function handleKeyDown(e) {
    if (e.key === 'Enter') {
      if (mainInput.length > 0) {
        addToDo(mainInput)
        setMainInput('')
      }
    }
  }

  // Cambia el filtro de tareas (todas, activas, completadas)
  function handleFilterChange(value) {
    setFilter(value)
    fetchTodos(value)
  }

  // Renderizado del componente
  return (
    <div className={styles.container}>
      <div className={styles.mainInputContainer}>
        {/* Input para crear una nueva tarea */}
        <input className={styles.mainInput} placeholder="What needs to be done?" value={mainInput} onChange={(e) => handleMainInputChange(e)} onKeyDown={handleKeyDown}></input>
      </div>
      {/* Mensaje de carga si no hay tareas */}
      {!todos && (
        <div>Loading...</div>
      )}
      {/* Renderiza cada tarea usando el componente ToDo */}
      {todos && (
        <div>
          {todos.map((todo) => {
            return (
              <ToDo key={todo.id} todo={todo} onDelete={handleDeleteToDo} onChange={handleToDoChange} />
            )
          })}
        </div>
      )}
      {/* Botones de filtro */}
      <div className={styles.filters}>
        <button className={`${styles.filterBtn} ${filter === undefined && styles.filterActive}`} onClick={() => handleFilterChange()}>All</button>
        <button className={`${styles.filterBtn} ${filter === false && styles.filterActive}`} onClick={() => handleFilterChange(false)}>Active</button>
        <button className={`${styles.filterBtn} ${filter === true && styles.filterActive}`} onClick={() => handleFilterChange(true)}>Completed</button>
      </div>
    </div>
  )
}