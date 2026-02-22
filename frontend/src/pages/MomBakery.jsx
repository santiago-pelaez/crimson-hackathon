import { useState, useEffect } from 'react'; // <-- MUST HAVE THIS!
import { Link } from 'react-router-dom';
import './MomBakery.css';

import img1 from '../images/2840.jpg';
import img2 from '../images/2841.jpg';
import img3 from '../images/2844.jpg';
import img4 from '../images/2846.jpg';

function MomBakery() {
  const images = [img1, img2, img3, img4];

  const [currentIndex, setCurrentIndex] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentIndex((prevIndex) => (prevIndex + 1) % images.length);
    }, 5000); 
    
    return () => clearInterval(timer); 
  }, [images.length]);

  return (
    <div className="bakery-container">
      
      <ul className="nav-links">
        {/* I changed "Log In" to "Worker Portal" and kept the link to /log_in */}
        <Link to="/log_in" className="log_in">Worker's Portal</Link>
        
        {/* I removed the "Sign Up" button completely */}
        
        <li className="cart-button"> View Cart 🛒</li>
      </ul>

      <main className="hero">
        
        <div className="hero-backgrounds">
          {images.map((img, index) => (
            <div
              key={index}
              className={`hero-bg-image ${index === currentIndex ? 'active' : ''}`}
              style={{ backgroundImage: `url(${img})` }}
            ></div>
          ))}
        </div>

        <div className="hero-content">
          <span>Since 1999</span>
          <h1>
            Freshly Cooked <br /> 
            <i>In The Matrix</i>
          </h1>
          <p>
            Hand-crafted sourdough and digital delights delivered with love 
            from our traditional stone oven to your screen.
          </p>
          <button className="hero-btn">Explore the Menu</button>
        </div>

        <div className="floating-deco deco-1">🌾</div>
        <div className="floating-deco deco-2">🥐</div>
        <div className="floating-deco deco-3">🌾</div>
        <div className="floating-deco deco-4">🥐</div>
        <div className="floating-deco deco-5">🌾</div>
        <div className="floating-deco deco-6">🥐</div>
      </main>

      <footer className="footer">
        <p>© 1999-2026 Mom's Artisanal Bakery Inc. All rights reserved.</p>
      
        <Link to="/login" className="secret-door">About us</Link>
      </footer>
    </div>
  );
}

export default MomBakery;