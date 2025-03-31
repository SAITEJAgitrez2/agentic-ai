"use client";

import { useEffect, useState } from "react";
import axios from "axios";

export default function LogsPage() {
  const [logs, setLogs] = useState<string[]>([]);

  useEffect(() => {
    const fetchLogs = async () => {
      try {
        const res = await axios.get("http://localhost:8000/api/logs");
        setLogs(res.data.logs);
      } catch (err) {
        console.error("Error fetching logs:", err);
      }
    };

    fetchLogs();
  }, []);

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-4">System Logs</h2>
      <div className="bg-gray-900 text-white p-4 rounded whitespace-pre-wrap">
        {logs.join("")}
      </div>
    </div>
  );
}
