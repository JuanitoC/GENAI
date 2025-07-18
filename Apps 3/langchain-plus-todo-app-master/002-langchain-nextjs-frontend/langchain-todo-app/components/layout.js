// layout.js
// Componente de layout general para la aplicación. Proporciona el marco visual y el título principal.

import styles from '../styles/layout.module.css'

export default function Layout(props) {
  return (
    <div className={styles.layout}>
      {/* Título principal de la app */}
      <h1 className={styles.title}>Full Stack App using ChatGPT</h1>
      {/* Subtítulo con créditos */}
      <p className={styles.subtitle}>By <a href="https://aiaccelera.com/" target="_blank">AI Accelera</a> and <a href="https://aceleradoraai.com/" target="_blank">Aceleradora AI</a></p>
      <p className={styles.subtitle}>Create Poems with your To Do Tasks</p>
      {/* Renderiza los hijos que se le pasen al layout */}
      {props.children}
    </div>
  )
}