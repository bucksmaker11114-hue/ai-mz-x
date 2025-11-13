import { useState, useEffect } from "react";

function App() {
  const [signal, setSignal] = useState(null);
  const [price, setPrice] = useState(null);
  const API_URL = import.meta.env.VITE_API_BASE_URL;
  const API_KEY = import.meta.env.VITE_API_KEY;

  useEffect(() => {
    const ws = new WebSocket(`${API_URL.replace("https", "wss")}/ws/live`);
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setPrice(data.price);
    };
    return () => ws.close();
  }, [API_URL]);

  const fetchSignal = async () => {
    const res = await fetch(`${API_URL}/api/analyze/EURUSD?key=${API_KEY}`);
    const data = await res.json();
    setSignal(data.result);
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-950 text-gray-100">
      <h1 className="text-3xl font-bold mb-6">AI Trading Dashboard</h1>
      <p className="text-xl mb-4">💹 Élő árfolyam: {price || "Betöltés..."}</p>
      <button
        onClick={fetchSignal}
        className="px-6 py-3 bg-blue-600 hover:bg-blue-700 rounded-xl shadow"
      >
        Friss AI jelzés
      </button>
      {signal && (
        <div className="mt-6 p-4 bg-gray-800 rounded-xl shadow-lg">
          <p>📊 Pár: {signal.pair}</p>
          <p>💡 Jelzés: {signal.signal}</p>
          <p>🎯 Bizalom: {signal.confidence}%</p>
          <p>⚙️ Modell: {signal.model}</p>
        </div>
      )}
    </div>
  );
}

export default App;
