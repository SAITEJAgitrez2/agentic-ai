"use client";

import { useEffect, useState } from "react";
import axios from "axios";

export default function ChatHistoryPage() {
  const [history, setHistory] = useState<any[]>([]);

  useEffect(() => {
    axios.get("http://localhost:8000/api/history?session_id=user").then(res => {
      setHistory(res.data.messages);
    });
  }, []);

  return (
    <main className="p-6">
      <h1 className="text-2xl font-bold mb-4">Chat History</h1>
      <div className="bg-white shadow-md p-4 rounded">
        {history.map((msg, idx) => (
          <div key={idx} className="mb-2">
            <p><strong>{msg.role === "user" ? "🧑‍💻 You" : "🤖 Assistant"}:</strong> {msg.content}</p>
          </div>
        ))}
      </div>
    </main>
  );
}
