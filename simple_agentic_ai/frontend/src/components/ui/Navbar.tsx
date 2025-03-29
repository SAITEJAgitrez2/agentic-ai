// src/app/components/ui/Navbar.tsx
"use client";

import Link from "next/link";

export default function Navbar() {
  return (
    <nav className="bg-slate-900 text-white p-4 flex gap-6">
      <Link href="/" className="hover:underline">Home</Link>
      <Link href="/history" className="hover:underline">Chat History</Link>
      <Link href="/logs" className="hover:underline">Logs</Link>
    </nav>
  );
}
