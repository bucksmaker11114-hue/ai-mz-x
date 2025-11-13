const API_BASE = import.meta.env.VITE_API_BASE_URL;

export async function fetchHealth() {
  const res = await fetch(`${API_BASE}/health`);
  return res.json();
}

export async function fetchSignal(pair) {
  const res = await fetch(`${API_BASE}/api/signal/${pair}`);
  return res.json();
}

export async function fetchAnalyze(pair) {
  const res = await fetch(`${API_BASE}/api/analyze/${pair}`);
  return res.json();
}

export async function fetchReport() {
  const res = await fetch(`${API_BASE}/api/report`);
  return res.json();
}
