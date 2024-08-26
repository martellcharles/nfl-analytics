import React from 'react';
import SeasonLeadersTable from './SeasonLeadersTable';
import styles from './HomePage.module.css'


const HomePage = () => {

  return (
    <div className={styles.homePage}>
      <div className={styles.hero}>
        <h1>Welcome to the NFL analytics page</h1>
        <p>Discover the power of analytics here</p>
        <SeasonLeadersTable />
      </div>
    </div>
  );
};

export default HomePage;