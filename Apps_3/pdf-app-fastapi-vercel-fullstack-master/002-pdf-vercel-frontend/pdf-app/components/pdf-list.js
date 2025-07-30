// pdf-list.js
// Componente principal para mostrar, filtrar, subir, editar y eliminar PDFs

import styles from '../styles/pdf-list.module.css';
import { useState, useEffect, useCallback, useRef } from 'react';
import { debounce } from 'lodash';
import PDFComponent from './pdf';

export default function PdfList() {
  // Estado para la lista de PDFs
  const [pdfs, setPdfs] = useState([]);
  // Estado para el archivo seleccionado para subir
  const [selectedFile, setSelectedFile] = useState(null);
  // Estado para el filtro de selección
  const [filter, setFilter] = useState();
  // Referencia para evitar múltiples fetchs
  const didFetchRef = useRef(false);

  // Cargar los PDFs al montar el componente
  useEffect(() => {
    if (!didFetchRef.current) {
      didFetchRef.current = true;
      fetchPdfs();
    }
  }, []);

  // Función para obtener los PDFs desde el backend, opcionalmente filtrando por 'selected'
  async function fetchPdfs(selected) {
    let path = '/pdfs';
    if (selected !== undefined) {
      path = `/pdfs?selected=${selected}`;
    }
    const res = await fetch(process.env.NEXT_PUBLIC_API_URL + path);
    const json = await res.json();
    setPdfs(json);
  }

  // Actualización de PDF con debounce para evitar llamadas excesivas
  const debouncedUpdatePdf = useCallback(debounce((pdf, fieldChanged) => {
    updatePdf(pdf, fieldChanged);
  }, 500), []);

  // Maneja el cambio de campos en un PDF (checkbox o texto)
  function handlePdfChange(e, id) {
    const target = e.target;
    const value = target.type === 'checkbox' ? target.checked : target.value;
    const name = target.name;
    const copy = [...pdfs];
    const idx = pdfs.findIndex((pdf) => pdf.id === id);
    const changedPdf = { ...pdfs[idx], [name]: value };
    copy[idx] = changedPdf;
    debouncedUpdatePdf(changedPdf, name);
    setPdfs(copy);
  }

  /*
    La función updatePdf envía el PDF completo al backend para actualizarlo.
    Es importante enviar todos los campos, no solo el modificado, para evitar errores en el backend.
  */
  async function updatePdf(pdf, fieldChanged) {
    const body_data = JSON.stringify(pdf);
    const url = process.env.NEXT_PUBLIC_API_URL + `/pdfs/${pdf.id}`;

    await fetch(url, {
        method: 'PUT',
        body: body_data,
        headers: { 'Content-Type': 'application/json' }
    });
  }

  // Elimina un PDF por su ID
  async function handleDeletePdf(id) {
    const res = await fetch(process.env.NEXT_PUBLIC_API_URL + `/pdfs/${id}`, {
      method: 'DELETE',
      headers: { 'Content-Type': 'application/json' }
    });

    if (res.ok) {
      const copy = pdfs.filter((pdf) => pdf.id !== id);
      setPdfs(copy);
    }
  }

  // Maneja el cambio de archivo a subir
  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  // Sube el archivo PDF seleccionado al backend
  const handleUpload = async (event) => {
    event.preventDefault();
    if (!selectedFile) {
      alert("Please select file to load.");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    const response = await fetch(process.env.NEXT_PUBLIC_API_URL + "/pdfs/upload", {
      method: "POST",
      body: formData,
    });

    if (response.ok) {
      const newPdf = await response.json();
      setPdfs([...pdfs, newPdf]);
    } else {
      alert("Error loading file.");
    }
  };

  // Cambia el filtro de PDFs (todos, seleccionados, no seleccionados)
  function handleFilterChange(value) {
    setFilter(value);
    fetchPdfs(value);
  }

  // Renderizado del componente
  return (
    <div className={styles.container}>
      <div className={styles.mainInputContainer}>
        {/* Formulario para subir un PDF */}
        <form onSubmit={handleUpload}>
          <input className={styles.mainInput} type="file" accept=".pdf" onChange={handleFileChange} />
          <button className={styles.loadBtn} type="submit">Load PDF</button>
        </form>
      </div>
      {/* Mensaje de carga si no hay PDFs */}
      {!pdfs.length && <div>Loading...</div>}
      {/* Renderiza cada PDF usando el componente PDFComponent */}
      {pdfs.map((pdf) => (
        <PDFComponent key={pdf.id} pdf={pdf} onDelete={handleDeletePdf} onChange={handlePdfChange} />
      ))}
      {/* Botones de filtro */}
      <div className={styles.filters}>
        <button className={`${styles.filterBtn} ${filter === undefined && styles.filterActive}`} onClick={() => handleFilterChange()}>See All</button>
        <button className={`${styles.filterBtn} ${filter === true && styles.filterActive}`} onClick={() => handleFilterChange(true)}>See Selected</button>
        <button className={`${styles.filterBtn} ${filter === false && styles.filterActive}`} onClick={() => handleFilterChange(false)}>See Not Selected</button>
      </div>
    </div>
  );
}
