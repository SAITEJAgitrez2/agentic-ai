'use client';

import { useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import ChatMessage from "@/components/ui/ChatMessage";
import axios from "axios";

export default function AssistantChat() {
  const [messages, setMessages] = useState<any[]>([]);
  const [input, setInput] = useState("");

  const sendMessage = async () => {
    if (!input.trim()) return;

    setMessages((prev) => [...prev, { role: "user", content: input }]);

    try {
      const res = await axios.post("http://localhost:8000/chat", { message: input });
      setMessages((prev) => [...prev, { role: "assistant", content: res.data.response }]);
    } catch (err) {
      setMessages((prev) => [...prev, { role: "assistant", content: "❌ Something went wrong!" }]);
    }

    setInput("");
  };

  return (
    <div className="max-w-2xl mx-auto p-4">
      <div className="space-y-2">
        {messages.map((msg, idx) => (
          <ChatMessage key={idx} role={msg.role} content={msg.content} />
        ))}
      </div>
      <div className="flex gap-2 mt-4">
        <Input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask something..."
        />
        <Button onClick={sendMessage}>Send</Button>
      </div>
    </div>
  );
}
