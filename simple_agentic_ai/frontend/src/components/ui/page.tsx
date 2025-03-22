// src/app/page.tsx
import dynamic from "next/dynamic";

const AssistantChat = dynamic(() => import("@/components/ui/AssistantChat"), { ssr: false });

export default function Home() {
  return (
    <main className="h-screen bg-slate-100 p-4">
      <h1 className="text-3xl font-bold text-center mb-6">🧠 Simple Agentic AI</h1>
      <AssistantChat />
    </main>
  );
}
