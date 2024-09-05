import React from 'react';
import { useNavigate } from 'react-router-dom';
import styles from './HomePage.module.css'

const HomePage = () => {
    const navigate = useNavigate();

  return (
    <div className={styles.homePage}>
      <div className={styles.hero}>
        <h1>Welcome to the sports analytics page</h1>
        <p>Discover the power of analytics here</p>
        <button onClick={() => navigate('/epl')} className={styles.button}>
            EPL
        </button>
        <button onClick={() => navigate('/mlb')} className={styles.button}>
            MLB
        </button>
        <button onClick={() => navigate('/nba')} className={styles.button}>
            NBA
        </button>
        <button onClick={() => navigate('/nfl')} className={styles.button}>
            NFL
        </button>
        <button onClick={() => navigate('/nhl')} className={styles.button}>
            NHL
        </button>
      </div>
    </div>
  );
};

export default HomePage;