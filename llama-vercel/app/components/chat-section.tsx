"use client";

import { useChat } from "ai/react";
import { ChatInput, ChatMessages } from "./ui/chat";

// Componente principal de la sección de chat
export default function ChatSection() {
  // Hook personalizado para manejar el estado y las acciones del chat
  const {
    messages,
    input,
    isLoading,
    handleSubmit,
    handleInputChange,
    reload,
    stop,
  } = useChat({ api: process.env.NEXT_PUBLIC_CHAT_API });

  // Renderiza los mensajes y el input del chat
  return (
    <div className="space-y-4 max-w-5xl w-full">
      <ChatMessages
        messages={messages}
        isLoading={isLoading}
        reload={reload}
        stop={stop}
      />
      <ChatInput
        input={input}
        handleSubmit={handleSubmit}
        handleInputChange={handleInputChange}
        isLoading={isLoading}
      />
    </div>
  );
}
