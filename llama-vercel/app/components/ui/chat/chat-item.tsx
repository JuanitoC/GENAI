"use client";

import ChatAvatar from "./chat-avatar";
import { Message } from "./chat-messages";

// Componente que representa un mensaje individual en el chat
export default function ChatItem(message: Message) {
  return (
    <div className="flex items-start gap-4 pt-5">
      <ChatAvatar {...message} />
      <p className="break-words">{message.content}</p>
    </div>
  );
}
