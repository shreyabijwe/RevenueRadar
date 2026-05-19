import React, { useState, useEffect } from 'react';
import KPICards from './KPICards';
import RevenueChart from './RevenueChart';
import BudgetChart from './BudgetChart';
import ForecastChart from './ForecastChart';
import YoYChart from './YoYChart';

const API = 'http://127.0.0.1:8000';

function Dashboard({ token, onLogout }) {
  const [kpis, setKpis] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activePage, setActivePage] = useState('Dashboard');

  const headers = {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json',
  };

  // eslint-disable-next-line
  useEffect(() => {
    fetch(`${API}/kpis`, { headers })
      .then(res => res.json())
      .then(data => { setKpis(data); setLoading(false); })
      .catch(() => setLoading(false));
  }, []);

  const navItems = ['Dashboard', 'Revenue', 'Budget', 'Forecast', 'Growth'];

  const renderPage = () => {
    switch (activePage) {
      case 'Revenue':   return <div style={styles.pageWrap}><h2 style={styles.pageTitle}>Revenue Analysis</h2><RevenueChart token={token} API={API} /></div>;
      case 'Budget':    return <div style={styles.pageWrap}><h2 style={styles.pageTitle}>Budget vs Actual</h2><BudgetChart token={token} API={API} /></div>;
      case 'Forecast':  return <div style={styles.pageWrap}><h2 style={styles.pageTitle}>Revenue Forecast</h2><ForecastChart token={token} API={API} /></div>;
      case 'Growth':    return <div style={styles.pageWrap}><h2 style={styles.pageTitle}>Year over Year Growth</h2><YoYChart token={token} API={API} /></div>;
      default: return (
        <>
          <KPICards kpis={kpis} />
          <div style={styles.row}>
            <RevenueChart token={token} API={API} />
            <ForecastChart token={token} API={API} />
          </div>
          <div style={styles.row}>
            <BudgetChart token={token} API={API} />
            <YoYChart token={token} API={API} />
          </div>
        </>
      );
    }
  };

  return (
    <div style={styles.container}>
      {/* Top Navbar */}
      <div style={styles.navbar}>
        <div style={styles.navLogo}>
          <span style={styles.navIcon}>📡</span>
          <span style={styles.navTitle}>RevenueRadar</span>
        </div>
        <div style={styles.navLinks}>
          {navItems.map(item => (
            <div
              key={item}
              onClick={() => setActivePage(item)}
              style={{
                ...styles.navLink,
                color: activePage === item ? '#F18F01' : '#8899aa',
                borderBottom: activePage === item ? '2px solid #F18F01' : '2px solid transparent',
              }}
            >
              {item}
            </div>
          ))}
        </div>
        <div style={styles.navRight}>
          <span style={styles.navDate}>{new Date().toDateString()}</span>
          <button onClick={onLogout} style={styles.logoutBtn}>Logout</button>
        </div>
      </div>

      {/* Main Content */}
      <div style={styles.main}>
        {loading ? (
          <p style={{ padding: '40px', color: '#F18F01' }}>Loading dashboard...</p>
        ) : (
          renderPage()
        )}
      </div>
    </div>
  );
}

const styles = {
  container: {
    minHeight: '100vh',
    background: '#0a0e1a',
  },
  navbar: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: '0 32px',
    height: '60px',
    background: '#0d1224',
    borderBottom: '1px solid rgba(241,143,1,0.2)',
    position: 'sticky',
    top: 0,
    zIndex: 100,
  },
  navLogo: {
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
  },
  navIcon: {
    fontSize: '20px',
  },
  navTitle: {
    fontSize: '18px',
    fontWeight: '700',
    color: '#F18F01',
    letterSpacing: '1px',
  },
  navLinks: {
    display: 'flex',
    gap: '8px',
  },
  navLink: {
    padding: '20px 16px',
    cursor: 'pointer',
    fontSize: '14px',
    fontWeight: '500',
    transition: 'color 0.2s',
  },
  navRight: {
    display: 'flex',
    alignItems: 'center',
    gap: '16px',
  },
  navDate: {
    fontSize: '12px',
    color: '#556677',
  },
  logoutBtn: {
    padding: '6px 14px',
    background: 'rgba(241,143,1,0.15)',
    color: '#F18F01',
    border: '1px solid rgba(241,143,1,0.3)',
    borderRadius: '6px',
    cursor: 'pointer',
    fontSize: '13px',
  },
  main: {
    padding: '24px 32px',
  },
  row: {
    display: 'grid',
    gridTemplateColumns: '1fr 1fr',
    gap: '24px',
    marginBottom: '24px',
  },
  pageWrap: {
    padding: '8px 0',
  },
  pageTitle: {
    fontSize: '22px',
    fontWeight: '700',
    color: '#F18F01',
    marginBottom: '24px',
  },
};

export default Dashboard;