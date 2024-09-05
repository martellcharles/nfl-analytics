import React from 'react';
import { useNavigate } from 'react-router-dom';
import styles from './TeamsPage.module.css'

const TeamsPage = () => {
    const navigate = useNavigate();

  return (
    <div className={styles.homePage}>
      <div className={styles.hero}>
        <h1>NFL Teams</h1>
        <p>Discover the power of analytics here</p>
        <button onClick={() => navigate('/epl')} className={styles.button}>
            EPL
        </button>
        <div>AFC</div>
        <div>NFC</div>
      </div>
    </div>
  );
};

export default TeamsPage;