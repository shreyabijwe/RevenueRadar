import React, { useState } from 'react';
import Login from './components/Login';
import Dashboard from './components/Dashboard';

function App() {
  const [token, setToken] = useState(localStorage.getItem('rr_token') || '');

  const handleLogin = (newToken) => {
    localStorage.setItem('rr_token', newToken);
    setToken(newToken);
  };

  const handleLogout = () => {
    localStorage.removeItem('rr_token');
    setToken('');
  };

  return (
    <div>
      {token ? (
        <Dashboard token={token} onLogout={handleLogout} />
      ) : (
        <Login onLogin={handleLogin} />
      )}
    </div>
  );
}

export default App;