import React, { useState } from 'react';

const API = 'http://127.0.0.1:8000';

function Login({ onLogin }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      const res = await fetch(`${API}/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
      });
      const data = await res.json();
      if (res.ok) {
        onLogin(data.access_token);
      } else {
        setError('Invalid username or password');
      }
    } catch (err) {
      setError('Cannot connect to server. Make sure the API is running.');
    }
    setLoading(false);
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <div style={styles.header}>
          <div style={styles.logo}>
            <span style={styles.logoIcon}>📡</span>
            <h1 style={styles.title}>RevenueRadar</h1>
          </div>
          <p style={styles.subtitle}>Financial Analytics Platform</p>
        </div>
        <form onSubmit={handleSubmit} style={styles.form}>
          <div style={styles.field}>
            <label style={styles.label}>Username</label>
            <input
              style={styles.input}
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Enter username"
              required
            />
          </div>
          <div style={styles.field}>
            <label style={styles.label}>Password</label>
            <input
              style={styles.input}
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter password"
              required
            />
          </div>
          {error && <p style={styles.error}>{error}</p>}
          <button style={styles.button} type="submit" disabled={loading}>
            {loading ? 'Authenticating...' : 'Access Dashboard'}
          </button>
          <p style={styles.hint}>Use: admin / radar2024</p>
        </form>
      </div>
    </div>
  );
}

const styles = {
  container: {
    minHeight: '100vh',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    background: 'linear-gradient(135deg, #0a0e1a 0%, #1a2340 50%, #0a0e1a 100%)',
  },
  card: {
    background: 'rgba(255,255,255,0.05)',
    borderRadius: '16px',
    padding: '48px 40px',
    width: '400px',
    boxShadow: '0 25px 60px rgba(0,0,0,0.5)',
    border: '1px solid rgba(241,143,1,0.3)',
    backdropFilter: 'blur(10px)',
  },
  header: {
    textAlign: 'center',
    marginBottom: '36px',
  },
  logo: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '10px',
    marginBottom: '8px',
  },
  logoIcon: {
    fontSize: '32px',
  },
  title: {
    fontSize: '28px',
    fontWeight: '700',
    color: '#F18F01',
    letterSpacing: '1px',
  },
  subtitle: {
    fontSize: '13px',
    color: '#8899aa',
    marginTop: '4px',
  },
  form: {
    display: 'flex',
    flexDirection: 'column',
    gap: '18px',
  },
  field: {
    display: 'flex',
    flexDirection: 'column',
    gap: '6px',
  },
  label: {
    fontSize: '12px',
    fontWeight: '600',
    color: '#F18F01',
    textTransform: 'uppercase',
    letterSpacing: '0.5px',
  },
  input: {
    padding: '12px 16px',
    borderRadius: '8px',
    border: '1px solid rgba(241,143,1,0.3)',
    fontSize: '14px',
    outline: 'none',
    background: 'rgba(255,255,255,0.05)',
    color: '#e0e6f0',
  },
  button: {
    padding: '14px',
    background: 'linear-gradient(135deg, #F18F01, #e67e00)',
    color: '#0a0e1a',
    border: 'none',
    borderRadius: '8px',
    fontSize: '15px',
    fontWeight: '700',
    cursor: 'pointer',
    marginTop: '8px',
    letterSpacing: '0.5px',
  },
  error: {
    color: '#e74c3c',
    fontSize: '13px',
    textAlign: 'center',
  },
  hint: {
    textAlign: 'center',
    fontSize: '12px',
    color: '#556677',
  },
};

export default Login;