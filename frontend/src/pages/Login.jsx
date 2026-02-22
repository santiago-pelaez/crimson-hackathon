import { useNavigate } from 'react-router-dom';
import './Login.css';

function Login() {
  const navigate = useNavigate();

  const handleLogin = async (e) => {
  e.preventDefault();
  
  // 1. Get the data from the form
  const username = e.target[0].value; 
  const password = e.target[1].value;

  // 2. Logic: Let's say only 'admin' with password 'password123' works
  const isSuccess = username === 'worker123' && password === 'password123';
  
  // 3. Prepare the payload for Gemini to analyze
  const loginData = {
    username: username,
    timestamp: new Date().toLocaleString(),
    status: isSuccess ? 'success' : 'failed',
    ip: '127.0.0.1', // Standard for local testing
    userAgent: navigator.userAgent // Cool extra info for Gemini!
  };

  try {
    // 4. Send this to your Python Backend
    await fetch('http://localhost:8000/log-event', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(loginData),
    });

    // 5. If successful, go to admin. If failed, maybe alert the user
    if (isSuccess) {
      navigate('/admin');
    } else {
      alert("AI Sentry: Unusual login detected. This attempt has been logged.");
    }
  } catch (error) {
    console.error("Backend offline!", error);
  }
};

  return (
    <div className="auth-container" alt='bakery store'>
      <div className="auth-card">
        <h2>Worker Portal</h2>
        <p style={{ color: '#7D5A50', opacity: 0.7, marginBottom: '20px' }}>
          Authorized Personnel Only. All access is monitored by Aegis Sentry AI.
        </p>
        <form onSubmit={handleLogin}>
          <div className="form-group">
            <label>Username</label>
            <input type="text" required />
          </div>
          <div className="form-group">
            <label>Password</label>
            <input type="password" required />
          </div>
          <button type="submit" className="auth-btn">Log In</button>
        </form>
      </div>
    </div>
  );
}

export default Login;