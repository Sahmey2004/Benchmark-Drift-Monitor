
const API_URL = import.meta.env.VITE_BDM_API_URL || 'http://localhost:8000';

export type Summary = {
  window: number;
  td_mean_bps: number;
  te_bps: number;
  count: number;
};

export type SeriesPoint = {
  date: string;
  fund_ret: number;
  bench_ret: number;
  td: number;
};

export async function runIngest(fund: string, benchmark: string, days = 120) {
  const res = await fetch(`${API_URL}/ingest/run?fund=${encodeURIComponent(fund)}&benchmark=${encodeURIComponent(benchmark)}&days=${days}`, { method: 'POST' });
  if (!res.ok) throw new Error('Ingest failed');
  return res.json();
}

export async function getSummary(fund: string, benchmark: string, window = 30): Promise<Summary> {
  const res = await fetch(`${API_URL}/metrics/summary?fund=${encodeURIComponent(fund)}&benchmark=${encodeURIComponent(benchmark)}&window=${window}`);
  if (!res.ok) throw new Error('Summary failed');
  return res.json();
}

export async function getSeries(fund: string, benchmark: string, window = 30): Promise<{points: SeriesPoint[]}> {
  const res = await fetch(`${API_URL}/metrics/series?fund=${encodeURIComponent(fund)}&benchmark=${encodeURIComponent(benchmark)}&window=${window}`);
  if (!res.ok) throw new Error('Series failed');
  return res.json();
}
