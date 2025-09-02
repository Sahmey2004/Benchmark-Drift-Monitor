
import React, { useEffect, useState } from 'react'
import { getSummary, getSeries, runIngest, SeriesPoint, Summary } from './api'
import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer, Legend } from 'recharts'

function fmtPct(x: number) { return (x*100).toFixed(2) + '%' }
function fmtBps(x: number) { return x.toFixed(1) + ' bps' }

export default function App() {
  const [fund, setFund] = useState('SPY')
  const [bm, setBm] = useState('^GSPC')
  const [window, setWindow] = useState(30)
  const [summary, setSummary] = useState<Summary | null>(null)
  const [series, setSeries] = useState<SeriesPoint[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function load() {
    setError(null); setLoading(true)
    try {
      const s = await getSummary(fund, bm, window)
      const ser = await getSeries(fund, bm, window)
      setSummary(s); setSeries(ser.points)
    } catch (e:any) {
      setError(e.message || 'Failed')
    } finally {
      setLoading(false)
    }
  }

  async function ingest() {
    setError(null); setLoading(true)
    try {
      await runIngest(fund, bm, 180)
      await load()
    } catch (e:any) {
      setError(e.message || 'Ingest failed')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [])

  const chartData = series.map(p => ({
    date: p.date.slice(0,10),
    fund_ret: p.fund_ret*100,
    bench_ret: p.bench_ret*100,
    td_bps: p.td*10000,
  }))

  return (
    <div style={{ padding: 24, maxWidth: 1100, margin: '0 auto', fontFamily: 'Inter, system-ui, Arial' }}>
      <h1 style={{ fontSize: 24, marginBottom: 8 }}>Benchmark Drift Monitor</h1>
      <p style={{ color: '#444', marginTop: 0 }}>Compute tracking difference (TD) and rolling tracking error (TE) for a fund vs its benchmark.</p>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr 1fr auto', gap: 12, alignItems: 'end', margin: '12px 0 24px' }}>
        <div>
          <label>Fund</label>
          <input value={fund} onChange={e=>setFund(e.target.value)} placeholder="SPY" style={{ width: '100%', padding: 8 }} />
        </div>
        <div>
          <label>Benchmark</label>
          <input value={bm} onChange={e=>setBm(e.target.value)} placeholder="^GSPC" style={{ width: '100%', padding: 8 }} />
        </div>
        <div>
          <label>Window (days)</label>
          <input type="number" value={window} onChange={e=>setWindow(parseInt(e.target.value||'30'))} style={{ width: '100%', padding: 8 }} />
        </div>
        <button onClick={load} disabled={loading} style={{ padding: '10px 12px' }}>Refresh</button>
        <button onClick={ingest} disabled={loading} style={{ padding: '10px 12px' }}>Ingest</button>
      </div>

      {error && <div style={{ background: '#fee', color: '#900', padding: 12, border: '1px solid #f99', marginBottom: 12 }}>{error}</div>}

      {summary && (
        <div style={{ display: 'flex', gap: 16, marginBottom: 16 }}>
          <div style={{ border: '1px solid #ddd', padding: 12, borderRadius: 8, minWidth: 220 }}>
            <div style={{ fontSize: 12, color: '#555' }}>Rolling Window</div>
            <div style={{ fontSize: 18, fontWeight: 600 }}>{summary.window} days</div>
          </div>
          <div style={{ border: '1px solid #ddd', padding: 12, borderRadius: 8, minWidth: 220 }}>
            <div style={{ fontSize: 12, color: '#555' }}>TD (mean)</div>
            <div style={{ fontSize: 18, fontWeight: 600 }}>{fmtBps(summary.td_mean_bps)}</div>
          </div>
          <div style={{ border: '1px solid #ddd', padding: 12, borderRadius: 8, minWidth: 220 }}>
            <div style={{ fontSize: 12, color: '#555' }}>TE (stdev of TD)</div>
            <div style={{ fontSize: 18, fontWeight: 600 }}>{fmtBps(summary.te_bps)}</div>
          </div>
        </div>
      )}

      <div style={{ height: 360, border: '1px solid #eee', borderRadius: 8, padding: 8, background: '#fff' }}>
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" hide />
            <YAxis yAxisId="left" label={{ value: 'Return %', angle: -90, position: 'insideLeft' }} />
            <YAxis yAxisId="right" orientation="right" label={{ value: 'TD (bps)', angle: -90, position: 'insideRight' }} />
            <Tooltip />
            <Legend />
            <Line yAxisId="left" type="monotone" dataKey="fund_ret" name="Fund Return (%)" dot={false} />
            <Line yAxisId="left" type="monotone" dataKey="bench_ret" name="Benchmark Return (%)" dot={false} />
            <Line yAxisId="right" type="monotone" dataKey="td_bps" name="TD (bps)" strokeDasharray="4 2" dot={false} />
          </LineChart>
        </ResponsiveContainer>
      </div>

      <div style={{ marginTop: 20, color: '#555', fontSize: 13 }}>
        <b>Explain Drift (lite):</b> TD measures difference in daily returns; TE is the rolling std of TD. Extend with fees, cash drag, concentration, and dividend timing for richer attribution.
      </div>
    </div>
  )
}
