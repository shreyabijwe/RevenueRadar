import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

function YoYChart({ token, API }) {
  const [data, setData] = useState([]);

  // eslint-disable-next-line
  useEffect(() => {
    fetch(`${API}/yoy-growth`, {
      headers: { 'Authorization': `Bearer ${token}` }
    })
      .then(res => res.json())
      .then(data => setData(data))
      .catch(() => {});
  }, []);

  return (
    <div style={styles.card}>
      <h3 style={styles.title}>Year over Year — Revenue, Expense, Profit (AED)</h3>
      <ResponsiveContainer width="100%" height={280}>
        <BarChart data={data} margin={{ top: 10, right: 10, left: 20, bottom: 10 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
          <XAxis dataKey="year" tick={{ fill: '#8899aa' }} />
          <YAxis tickFormatter={(v) => `${(v / 1e6).toFixed(1)}M`} tick={{ fill: '#8899aa' }} />
          <Tooltip
            formatter={(value) => `AED ${value.toLocaleString()}`}
            contentStyle={{ background: '#0d1224', border: '1px solid #F18F01', borderRadius: '8px' }}
            labelStyle={{ color: '#F18F01' }}
          />
          <Legend />
          <Bar dataKey="revenue" name="Revenue" fill="#F18F01" radius={[4, 4, 0, 0]} />
          <Bar dataKey="expense" name="Expense" fill="#e74c3c" radius={[4, 4, 0, 0]} />
          <Bar dataKey="profit" name="Profit" fill="#27ae60" radius={[4, 4, 0, 0]} />
        </BarChart>
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

export default YoYChart;