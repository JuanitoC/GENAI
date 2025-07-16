// _document.js
// Estructura HTML base personalizada para la app Next.js

import { Html, Head, Main, NextScript } from 'next/document'

export default function Document() {
  return (
    <Html lang="en">
      <Head />
      <body>
        {/* Renderiza el contenido principal de la app */}
        <Main />
        {/* Scripts de Next.js necesarios para el funcionamiento */}
        <NextScript />
      </body>
    </Html>
  )
}
