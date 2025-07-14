import {
  ContextChatEngine,
  LLM,
  serviceContextFromDefaults,
  SimpleDocumentStore,
  storageContextFromDefaults,
  VectorStoreIndex,
} from "llamaindex";
import { CHUNK_OVERLAP, CHUNK_SIZE, STORAGE_CACHE_DIR } from "./constants.mjs";

// Obtiene la fuente de datos (índice) a partir del almacenamiento persistente y el modelo LLM
async function getDataSource(llm: LLM) {
  const serviceContext = serviceContextFromDefaults({
    llm,
    chunkSize: CHUNK_SIZE,
    chunkOverlap: CHUNK_OVERLAP,
  });
  let storageContext = await storageContextFromDefaults({
    persistDir: `${STORAGE_CACHE_DIR}`,
  });

  // Verifica que existan documentos en el almacenamiento
  const numberOfDocs = Object.keys(
    (storageContext.docStore as SimpleDocumentStore).toDict(),
  ).length;
  if (numberOfDocs === 0) {
    throw new Error(
      `StorageContext is empty - call 'npm run generate' to generate the storage first`,
    );
  }
  // Inicializa el índice vectorial con el contexto de almacenamiento y servicio
  return await VectorStoreIndex.init({
    storageContext,
    serviceContext,
  });
}

// Crea el motor de chat usando el índice y el modelo LLM
export async function createChatEngine(llm: LLM) {
  const index = await getDataSource(llm);
  const retriever = index.asRetriever();
  retriever.similarityTopK = 5;

  return new ContextChatEngine({
    chatModel: llm,
    retriever,
  });
}
