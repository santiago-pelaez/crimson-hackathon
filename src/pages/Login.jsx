import { useNavigate } from 'react-router-dom';
import './Login.css';

function Login() {
  const navigate = useNavigate();

  const handleLogin = (e) => {
    e.preventDefault();
   
    setTimeout(() => {
      navigate('/admin');
    }, 1000);
  };

  return (
    <div className="auth-container" alt='bakery store'>
      <div className="auth-card">
        <h2>User Portal</h2>
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