import { Message, StreamingTextResponse } from "ai";
import { OpenAI } from "llamaindex";
import { NextRequest, NextResponse } from "next/server";
import { createChatEngine } from "./engine";
import { LlamaIndexStream } from "./llamaindex-stream";

// Configuración del runtime para Next.js
export const runtime = "nodejs";
export const dynamic = "force-dynamic";

// Maneja las peticiones POST para el endpoint de chat
export async function POST(request: NextRequest) {
  try {
    // Extrae los mensajes del cuerpo de la petición
    const body = await request.json();
    const { messages }: { messages: Message[] } = body;
    const lastMessage = messages.pop();
    if (!messages || !lastMessage || lastMessage.role !== "user") {
      return NextResponse.json(
        {
          error:
            "messages are required in the request body and the last message must be from the user",
        },
        { status: 400 },
      );
    }

    // Inicializa el modelo LLM de OpenAI
    const llm = new OpenAI({
      model: "gpt-3.5-turbo",
    });

    // Crea el motor de chat usando el modelo
    const chatEngine = await createChatEngine(llm);

    // Genera la respuesta del chat de manera asíncrona y en streaming
    const response = await chatEngine.chat(lastMessage.content, messages, true);

    // Transforma la respuesta en un stream legible por el cliente
    const stream = LlamaIndexStream(response);

    // Devuelve la respuesta en streaming al cliente
    return new StreamingTextResponse(stream);
  } catch (error) {
    // Manejo de errores
    console.error("[LlamaIndex]", error);
    return NextResponse.json(
      {
        error: (error as Error).message,
      },
      {
        status: 500,
      },
    );
  }
}
