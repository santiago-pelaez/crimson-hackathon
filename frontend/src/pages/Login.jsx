import { useNavigate } from 'react-router-dom';
import { useState } from 'react';
import './Login.css';

function Login() {
  const navigate = useNavigate();
  const [errorMsg, setErrorMsg] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();

    const formData = new FormData(e.currentTarget);
    const username = formData.get('username'); 
    const password = formData.get('password'); 

    console.log("Attempting login for:", username); 

    const isSuccess = username === 'worker123' && password === 'password123';
    
    const loginData = {
      username: username || "anonymous",
      timestamp: new Date().toISOString(),
      status: isSuccess ? 'success' : 'failed',
      location: 'West Coast, US', 
      isVPN: false,
      ip: '127.0.0.1',
      userAgent: navigator.userAgent
    };

    // --- REPLACED BLOCK START ---
    try {
      await fetch('http://localhost:8000/log-event', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(loginData),
      });
      
      if (isSuccess) {
        console.log("Login Success! Moving to Admin...");
        navigate('/admin'); 
      } else {
        setErrorMsg("ACCESS DENIED: Invalid Credentials.");
      }
    } catch (error) {
      console.error("Backend error, but bypassing for demo...");
      if (isSuccess) navigate('/admin'); 
    }
    // --- REPLACED BLOCK END ---
  };

  return (
    <div className="auth-container-serious">
      <div className="auth-card">
        <h2>Aegis Secure Portal</h2>
        <p className="auth-subtitle">Quantum-Resistant Authentication System</p>
        
        {errorMsg && <div className="error-banner">{errorMsg}</div>}

        <form onSubmit={handleLogin}>
          <div className="form-group">
            <label>Employee ID</label>
            <input name="username" type="text" placeholder="Username" required />
          </div>
          <div className="form-group">
            <label>Security Key</label>
            <input name="password" type="password" placeholder="••••••••" required />
          </div>
          <button type="submit" className="auth-btn-serious">SECURE ACCESS</button>
        </form>
      </div>
    </div>
  ); 
}

export default Login;