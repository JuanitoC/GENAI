"use client";

export interface ChatInputProps {
  /** Valor actual del input */
  input?: string;
  /** Manejador para el cambio de valor del input/textarea */
  handleInputChange?: (
    e:
      | React.ChangeEvent<HTMLInputElement>
      | React.ChangeEvent<HTMLTextAreaElement>,
  ) => void;
  /** Manejador para el envío del formulario */
  handleSubmit: (e: React.FormEvent<HTMLFormElement>) => void;
  isLoading: boolean;
}

// Componente de input para enviar mensajes al chat
export default function ChatInput(props: ChatInputProps) {
  return (
    <>
      <form
        onSubmit={props.handleSubmit}
        className="flex items-start justify-between w-full max-w-5xl p-4 bg-white rounded-xl shadow-xl gap-4"
      >
        <input
          autoFocus
          name="message"
          placeholder="Type a message"
          className="w-full p-4 rounded-xl shadow-inner flex-1"
          value={props.input}
          onChange={props.handleInputChange}
        />
        <button
          disabled={props.isLoading}
          type="submit"
          className="p-4 text-white rounded-xl shadow-xl bg-gradient-to-r from-cyan-500 to-sky-500 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Send message
        </button>
      </form>
    </>
  );
}
