import { useNavigate } from 'react-router-dom';
import { useState } from 'react';
import './Login.css';

function Login() {
  const navigate = useNavigate();
  const [errorMsg, setErrorMsg] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();

    // This is the more reliable way to get data from the form
    const formData = new FormData(e.currentTarget);
    const username = formData.get('username'); // Make sure your input has name="username"
    const password = formData.get('password'); // Make sure your input has name="password"

    console.log("Attempting login for:", username); // Debug line

    const isSuccess = username === 'worker123' && password === 'password123';
    
    const loginData = {
      username: username || "anonymous", // Fallback so it's never null
      timestamp: new Date().toISOString(),
      status: isSuccess ? 'success' : 'failed',
      location: 'West Coast, US', 
      isVPN: false,
      ip: '127.0.0.1',
      userAgent: navigator.userAgent
    };

    // ... rest of your fetch code ...
    try {
      const response = await fetch('http://localhost:8000/log-event', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(loginData),
      });
      
      const result = await response.json();

      if (isSuccess && result.analysis.queue !== "Yellow") {
        navigate('/admin');
      } else if (result.analysis.queue === "Yellow") {
        setErrorMsg("LOGIN HELD: Domestic VPN detected. Pending Admin Approval.");
      } else {
        setErrorMsg(`ACCESS DENIED: Attempt logged. Threat Score: ${result.analysis.score}`);
      }
    } catch (error) {
      console.error("Backend offline!");
    }
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
  ); // <--- Added this );
} // <--- Added this }

export default Login;