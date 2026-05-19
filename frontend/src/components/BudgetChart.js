import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ReferenceLine } from 'recharts';

function BudgetChart({ token, API }) {
  const [data, setData] = useState([]);

  // eslint-disable-next-line
  useEffect(() => {
    fetch(`${API}/budget-vs-actual`, {
      headers: { 'Authorization': `Bearer ${token}` }
    })
      .then(res => res.json())
      .then(data => setData(data))
      .catch(() => {});
  }, []);

  return (
    <div style={styles.card}>
      <h3 style={styles.title}>Budget vs Actual Revenue (AED)</h3>
      <ResponsiveContainer width="100%" height={280}>
        <BarChart data={data} margin={{ top: 10, right: 10, left: 20, bottom: 60 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
          <XAxis dataKey="department" angle={-35} textAnchor="end" tick={{ fontSize: 11, fill: '#8899aa' }} />
          <YAxis tickFormatter={(v) => `${(v / 1e6).toFixed(1)}M`} tick={{ fill: '#8899aa' }} />
          <Tooltip
            formatter={(value) => `AED ${value.toLocaleString()}`}
            contentStyle={{ background: '#0d1224', border: '1px solid #F18F01', borderRadius: '8px' }}
            labelStyle={{ color: '#F18F01' }}
          />
          <Legend />
          <Bar dataKey="actual_revenue" name="Actual Revenue" fill="#F18F01" radius={[4, 4, 0, 0]} />
          <Bar dataKey="budget_revenue" name="Budget Revenue" fill="#2E86AB" radius={[4, 4, 0, 0]} />
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

export default BudgetChart;