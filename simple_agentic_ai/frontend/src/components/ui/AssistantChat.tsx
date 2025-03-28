"use client";

import { useState } from "react";
import axios from "axios";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

export default function AssistantChat() {
  const [messages, setMessages] = useState<any[]>([]);
  const [input, setInput] = useState("");
  const [pdfUrl, setPdfUrl] = useState("");
  const [pdfFile, setPdfFile] = useState<File | null>(null);

  const sendMessage = async () => {
    if (!input.trim()) return;

    setMessages((prev) => [...prev, { role: "user", content: input }]);

    try {
      const res = await axios.post("http://localhost:8000/api/chat", {
        message: input,
        user: "user",
      });
      setMessages((prev) => [...prev, { role: "assistant", content: res.data.response }]);
    } catch (err) {
      setMessages((prev) => [...prev, { role: "assistant", content: "❌ Error: Could not reach backend." }]);
    }

    setInput("");
  };

  const ingestPdfUrl = async () => {
    if (!pdfUrl.trim()) return;
    try {
      await axios.post("http://localhost:8000/api/ingest/url", { pdf_urls: [pdfUrl] });
      alert("PDF successfully ingested!");
    } catch (err) {
      alert("Error ingesting PDF.");
    }
    setPdfUrl("");
  };

  const ingestPdfFile = async () => {
    if (!pdfFile) return;
    const formData = new FormData();
    formData.append("file", pdfFile);
    
    try {
      await axios.post("http://localhost:8000/api/ingest/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      alert("PDF successfully uploaded!");
    } catch (err) {
      alert("Error uploading PDF.");
    }
  };

  return (
    <Card className="p-4 w-full max-w-2xl mx-auto bg-slate-100">
      <h2 className="text-2xl font-bold mb-2">Agentic AI Assistant</h2>
      
      <div className="space-y-2 mb-4 h-60 overflow-y-auto border p-2">
        {messages.map((msg, i) => (
          <p key={i} className={msg.role === "user" ? "text-right text-blue-600" : "text-left text-gray-800"}>
            {msg.role === "user" ? "🧑‍💻" : "🤖"} {msg.content}
          </p>
        ))}
      </div>

      <div className="flex space-x-2">
        <Input
          placeholder="Type a message..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
        />
        <Button onClick={sendMessage}>Send</Button>
      </div>

      <div className="mt-4 space-y-2">
        <Input
          placeholder="Enter PDF URL..."
          value={pdfUrl}
          onChange={(e) => setPdfUrl(e.target.value)}
        />
        <Button onClick={ingestPdfUrl}>Ingest PDF URL</Button>

        <input
          type="file"
          accept="application/pdf"
          onChange={(e) => setPdfFile(e.target.files?.[0] || null)}
        />
        <Button onClick={ingestPdfFile}>Upload PDF</Button>
      </div>
    </Card>
  );
}
