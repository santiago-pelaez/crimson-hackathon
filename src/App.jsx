import { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';      
import Admin from './pages/Admin';      
import MomBakery from './pages/MomBakery';
import Login from './pages/Login'

function App() {
  const [isLocked, setIsLocked] = useState(false);
  const [threatLevel, setThreatLevel] = useState(0);   

  useEffect(() => {
    const interval = setInterval(async () => {
      try {
        const res = await fetch('http://localhost:8000/status'); 
        const data = await res.json();
        setIsLocked(data.locked);
        setThreatLevel(data.threat_level || 0);
      } catch (e) {
        console.log("Backend not ready yet — using mock");
      }
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  return (
    <Router>
      <Routes>
        <Route path="/shop" element={<MomBakery />} />   
        <Route path="/log_in" element={<Login />} />
        <Route path="/sign_up" element={<Login />} />
        <Route path="/admin" element={
          <Admin 
            isLocked={isLocked} 
            threatLevel={threatLevel}
            setIsLocked={setIsLocked} 
          />
        } />
        <Route path="/honeypot" element={<Admin isLocked={true} threatLevel={80} />} /> 
      </Routes>
    </Router>
  );
}

export default App;