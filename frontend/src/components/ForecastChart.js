import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts';

function ForecastChart({ token, API }) {
  const [data, setData] = useState([]);

  // eslint-disable-next-line
  useEffect(() => {
    fetch(`${API}/forecast`, {
      headers: { 'Authorization': `Bearer ${token}` }
    })
      .then(res => res.json())
      .then(data => setData(data))
      .catch(() => {});
  }, []);

  return (
    <div style={styles.card}>
      <h3 style={styles.title}>Revenue Forecast — Next 6 Months (AED)</h3>
      <ResponsiveContainer width="100%" height={280}>
        <LineChart data={data} margin={{ top: 10, right: 20, left: 20, bottom: 20 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
          <XAxis dataKey="date" tick={{ fontSize: 11, fill: '#8899aa' }} />
          <YAxis tickFormatter={(v) => `${(v / 1e6).toFixed(1)}M`} tick={{ fill: '#8899aa' }} />
          <Tooltip
            formatter={(value) => `AED ${value.toLocaleString()}`}
            contentStyle={{ background: '#0d1224', border: '1px solid #27ae60', borderRadius: '8px' }}
            labelStyle={{ color: '#27ae60' }}
          />
          <Line
            type="monotone"
            dataKey="forecasted_revenue"
            name="Forecasted Revenue"
            stroke="#27ae60"
            strokeWidth={3}
            dot={{ fill: '#27ae60', r: 6 }}
            strokeDasharray="6 3"
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

const styles = {
  card: {
    background: '#0d1224',
    borderRadius: '10px',
    padding: '20px',
    border: '1px solid rgba(255,255,255,0.05)',
  },
  title: {
    fontSize: '14px',
    fontWeight: '600',
    color: '#F18F01',
    marginBottom: '16px',
  },
};

export default ForecastChart;