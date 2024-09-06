import React from 'react';
import { useNavigate } from 'react-router-dom';
import styles from './HomePage.module.css'

const sports = [
  { name: 'EPL', route: '/epl', description: 'English Premier League' },
  { name: 'MLB', route: '/mlb', description: 'Major League Baseball' },
  { name: 'NBA', route: '/nba', description: 'National Basketball Association' },
  { name: 'NFL', route: '/nfl', description: 'National Football League' },
  { name: 'NHL', route: '/nhl', description: 'National Hockey League' },
];

const HomePage = () => {
  const navigate = useNavigate();

  return (
    <div className={styles.homePage}>
      <div className={styles.hero}>
        <h1 className={styles.title}>Welcome to the Sports Analytics Page</h1>
        <p className={styles.subtitle}>Discover the power of analytics here</p>
      </div>
      <div className={styles.sportsGrid}>
        {sports.map((sport) => (
          <div key={sport.name} className={styles.sportCard} onClick={() => navigate(sport.route)}>
            <h2 className={styles.sportName}>{sport.name}</h2>
            <p className={styles.sportDescription}>{sport.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default HomePage;