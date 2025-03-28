// src/app/lib/api.ts
export async function sendMessage(message: string, session_id: string = "user") {
    const res = await fetch("http://localhost:8000/api/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message, session_id }),
    });
  
    const data = await res.json();
    return data.response;
  }
  