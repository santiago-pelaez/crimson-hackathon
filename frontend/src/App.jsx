import { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Admin from './pages/Admin';
import MomBakery from './pages/MomBakery';
import Login from './pages/Login'

function App() {
  const [isLocked, setIsLocked] = useState(false);
  const [threatLevel, setThreatLevel] = useState(0);
  const [aiThoughts, setAiThoughts] = useState("Monitoring..."); // <--- ADD THIS

  useEffect(() => {
    const interval = setInterval(async () => {
      try {
        const res = await fetch('http://localhost:8000/status');
        const data = await res.json();
        setIsLocked(data.is_locked);
        setThreatLevel(data.threat_level || 0);
        setAiThoughts(data.ai_thoughts || "System stable."); // <--- ADD THIS
      } catch (e) {
        console.log("Backend not ready yet");
      }
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  return (
    <Router>
      <Routes>
        <Route path="/" element={<MomBakery />} />
        <Route path="/login" element={<Login />} />
        <Route path="/log_in" element={<Login />} />
        <Route path="/sign_up" element={<Login />} />
        <Route path="/admin" element={
          <Admin 
            isLocked={isLocked} 
            threatLevel={threatLevel} 
            aiThoughts={aiThoughts} // <--- ADD THIS
          />
        } />
        <Route path="/honeypot" element={<Admin isLocked={true} threatLevel={80} />} />
      </Routes>
    </Router>
  );
}

export default App;