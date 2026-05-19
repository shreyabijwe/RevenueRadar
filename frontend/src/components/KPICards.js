import React from 'react';

function KPICards({ kpis }) {
  if (!kpis) return null;

  const cards = [
    { label: 'Total Revenue', value: `AED ${(kpis.total_revenue / 1e6).toFixed(2)}M`, icon: '💰', color: '#F18F01' },
    { label: 'Total Expense', value: `AED ${(kpis.total_expense / 1e6).toFixed(2)}M`, icon: '📊', color: '#e74c3c' },
    { label: 'Total Profit', value: `AED ${(kpis.total_profit / 1e6).toFixed(2)}M`, icon: '📈', color: '#27ae60' },
    { label: 'Avg Profit Margin', value: `${kpis.avg_profit_margin}%`, icon: '🎯', color: '#2E86AB' },
    { label: 'Best Department', value: kpis.best_department, icon: '🏆', color: '#F18F01' },
    { label: 'Latest Year Revenue', value: `AED ${(kpis.latest_year_revenue / 1e6).toFixed(2)}M`, icon: '📅', color: '#8e44ad' },
  ];

  return (
    <div style={styles.grid}>
      {cards.map((card, i) => (
        <div key={i} style={{ ...styles.card, borderLeft: `4px solid ${card.color}` }}>
          <div style={styles.cardTop}>
            <span style={styles.icon}>{card.icon}</span>
            <span style={{ ...styles.value, color: card.color }}>{card.value}</span>
          </div>
          <div style={styles.label}>{card.label}</div>
        </div>
      ))}
    </div>
  );
}

const styles = {
  grid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(3, 1fr)',
    gap: '16px',
    marginBottom: '24px',
  },
  card: {
    background: '#0d1224',
    borderRadius: '10px',
    padding: '20px',
    border: '1px solid rgba(255,255,255,0.05)',
  },
  cardTop: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '8px',
  },
  icon: {
    fontSize: '24px',
  },
  value: {
    fontSize: '20px',
    fontWeight: '700',
  },
  label: {
    fontSize: '12px',
    color: '#556677',
    textTransform: 'uppercase',
    letterSpacing: '0.5px',
  },
};

export default KPICards;