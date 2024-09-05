import React from 'react';
// import SeasonLeadersTable from '../../components/nba/SeasonLeadersTable';
import styles from './HomePage.module.css'


const NbaHomePage = () => {

  return (
    <div className={styles.homePage}>
      <div className={styles.hero}>
        <h1>Welcome to the NBA analytics page</h1>
        <p>Discover the power of analytics here</p>
        <p>Coming soon!</p>
        {/* <SeasonLeadersTable /> */}
      </div>
    </div>
  );
};

export default NbaHomePage;