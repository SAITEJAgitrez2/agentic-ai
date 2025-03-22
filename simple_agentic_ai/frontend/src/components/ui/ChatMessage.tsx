type ChatMessageProps = {
    role: string;
    content: string;
  };
  
  export default function ChatMessage({ role, content }: ChatMessageProps) {
    return (
      <div className={`p-3 rounded-xl ${role === "user" ? "bg-slate-200 text-black" : "bg-slate-800 text-white"}`}>
        <p><strong>{role === "user" ? "You" : "Assistant"}:</strong> {content}</p>
      </div>
    );
  }
  