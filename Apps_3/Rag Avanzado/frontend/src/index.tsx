// index.tsx
// Punto de entrada de la app React. Monta el componente principal en el DOM.

import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

// Si quieres medir el rendimiento de la app, puedes pasar una función a reportWebVitals
// para registrar resultados o enviarlos a un endpoint de analítica.
reportWebVitals();
