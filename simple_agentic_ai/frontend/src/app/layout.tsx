// src/app/layout.tsx
import type { Metadata } from "next";
import { Inter, Roboto_Mono } from "next/font/google";
import "./globals.css";
import Navbar from "@/components/ui/Navbar";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-sans",
});

const robotoMono = Roboto_Mono({
  subsets: ["latin"],
  variable: "--font-mono",
});

export const metadata: Metadata = {
  title: "Simple Agentic AI Assistant",
  description: "Chat interface powered by a PDF-based RAG assistant",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${inter.variable} ${robotoMono.variable} antialiased`}>
        <Navbar />
        <main className="p-6">{children}</main>
      </body>
    </html>
  );
}
