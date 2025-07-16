// _app.js
// Archivo de inicialización global de la app Next.js. Aplica estilos globales y renderiza la página correspondiente.

import '@/styles/globals.css'

export default function App({ Component, pageProps }) {
  // Renderiza el componente de página con sus props
  return <Component {...pageProps} />
}
