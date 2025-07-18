// index.js
// Página principal de la app. Muestra el layout y la lista de tareas (ToDo).

import Head from 'next/head'
import Layout from '../components/layout';
import ToDoList from '../components/todo-list';

export default function Home() {
  return (
    <div>
      {/* Metadatos de la página */}
      <Head>
        <title>LangChain Full Stack To Do App</title>
        <meta name="description" content="Full Stack Book To Do" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      {/* Layout general y lista de tareas */}
      <Layout>
        <ToDoList />
      </Layout>
    </div>
  )
}