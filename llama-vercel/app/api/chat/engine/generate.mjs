import {
  serviceContextFromDefaults,
  SimpleDirectoryReader,
  storageContextFromDefaults,
  VectorStoreIndex,
} from "llamaindex";

import * as dotenv from "dotenv";

import {
  CHUNK_OVERLAP,
  CHUNK_SIZE,
  STORAGE_CACHE_DIR,
  STORAGE_DIR,
} from "./constants.mjs";

// Carga las variables de entorno desde un archivo .env local
dotenv.config();

// Función auxiliar para medir el tiempo de ejecución de una función asíncrona
async function getRuntime(func) {
  const start = Date.now();
  await func();
  const end = Date.now();
  return end - start;
}

// Genera la fuente de datos procesando los documentos y almacenando los embeddings
async function generateDatasource(serviceContext) {
  console.log(`Generating storage context...`);
  // Divide los documentos, crea los embeddings y los almacena en el storage context
  const ms = await getRuntime(async () => {
    const storageContext = await storageContextFromDefaults({
      persistDir: STORAGE_CACHE_DIR,
    });
    const documents = await new SimpleDirectoryReader().loadData({
      directoryPath: STORAGE_DIR,
    });
    await VectorStoreIndex.fromDocuments(documents, {
      storageContext,
      serviceContext,
    });
  });
  console.log(`Storage context successfully generated in ${ms / 1000}s.`);
}

// Ejecución principal del script para generar el almacenamiento
(async () => {
  const serviceContext = serviceContextFromDefaults({
    chunkSize: CHUNK_SIZE,
    chunkOverlap: CHUNK_OVERLAP,
  });

  await generateDatasource(serviceContext);
  console.log("Finished generating storage.");
})();
