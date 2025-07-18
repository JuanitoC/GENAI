// pdf.js
// Componente para renderizar un PDF individual con opciones de edición, selección, visualización y borrado

import Image from 'next/image';
import styles from '../styles/pdf.module.css';

export default function PDFComponent(props) {
  // Recibe el PDF, y los handlers para cambio y borrado
  const { pdf, onChange, onDelete } = props;
  return (
    <div className={styles.pdfRow}>
      {/* Checkbox para marcar como seleccionado */}
      <input
        className={styles.pdfCheckbox}
        name="selected"
        type="checkbox"
        checked={pdf.selected}
        onChange={(e) => onChange(e, pdf.id)}
      />
      {/* Campo editable para el nombre del PDF */}
      <input
        className={styles.pdfInput}
        autoComplete="off"
        name="name"
        type="text"
        value={pdf.name}
        onChange={(e) => onChange(e, pdf.id)}
      />
      {/* Enlace para ver el PDF en una nueva pestaña */}
      <a
        href={pdf.file}
        target="_blank"
        rel="noopener noreferrer"
        className={styles.viewPdfLink}
      >
        <Image src="/document-view.svg" width="22" height="22" />
      </a>
      {/* Botón para eliminar el PDF */}
      <button
        className={styles.deleteBtn}
        onClick={() => onDelete(pdf.id)}
      >
        <Image src="/delete-outline.svg" width="24" height="24" />
      </button>
    </div>
  );
}
