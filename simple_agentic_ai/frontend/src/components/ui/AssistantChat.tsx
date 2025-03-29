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
  const [isLoading, setIsLoading] = useState(false);


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
  {isLoading && (
    <p className="text-sm text-gray-500 animate-pulse mb-2">📥 Ingesting PDF... Please wait</p>
  )}
  

  const ingestPdfUrl = async () => {
    if (!pdfUrl.trim()) return;
  
    const urls = pdfUrl
      .split(/[\n,]+/) // split on commas or newlines
      .map((u) => u.trim())
      .filter((u) => u.length > 0);
  
    if (urls.length === 0) {
      alert("Please enter at least one valid URL.");
      return;
    }
  
    setIsLoading(true);
    try {
      const response = await axios.post("http://localhost:8000/api/ingest/url", {
        pdf_urls: urls,
      });
      alert(response.data.message || "PDF(s) successfully ingested!");
      setIsLoading(false);
    } catch (err: any) {
      const error = err.response?.data?.detail || "Error ingesting PDF(s).";
      alert(error);
    } finally {
      setPdfUrl("");
    }
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
        {isLoading && (
  <div className="flex items-center space-x-2 mb-2">
    <div className="w-4 h-4 border-2 border-t-transparent border-blue-500 rounded-full animate-spin"></div>
    <span className="text-sm text-gray-600">Processing...</span>
  </div>
)}

        <Button onClick={ingestPdfUrl} disabled={isLoading}>
          {isLoading ? "Ingesting..." : "Ingest PDF URL"}
        </Button>


        <Button
  disabled={isLoading}
  onClick={() => {
    const fileInput = document.createElement("input");
    fileInput.type = "file";
    fileInput.accept = "application/pdf";
    fileInput.onchange = async (e: any) => {
      const file = e.target.files?.[0];
      if (!file) return;
      const formData = new FormData();
      formData.append("file", file);

      try {
        setIsLoading(true);
        await axios.post("http://localhost:8000/api/ingest/upload", formData, {
          headers: { "Content-Type": "multipart/form-data" },
        });
        alert("✅ PDF uploaded and ingested!");
      } catch (err: any) {
        alert("❌ Upload failed: " + (err?.response?.data?.detail || "Unknown error"));
      } finally {
        setIsLoading(false);
      }
    };
    fileInput.click(); // Trigger the file picker
  }}
>
  {isLoading ? (
    <div className="flex items-center space-x-2">
      <div className="w-3 h-3 border-2 border-white border-t-transparent rounded-full animate-spin" />
      <span>Uploading...</span>
    </div>
  ) : (
    "Upload PDF"
  )}
</Button>


      </div>
    </Card>
  );
}
