import React from 'react';
import Header from '../../components/nfl/Header';
import SeasonLeadersTable from '../../components/nfl/SeasonLeadersTable';
import styles from './HomePage.module.css'


const NflHomePage = () => {

  return (
    <div className={styles.homePage}>
      <Header />
      <div className={styles.hero}>
        <h1>Welcome to the NFL analytics page</h1>
        <p>Discover the power of analytics here</p>
        <SeasonLeadersTable />
      </div>
    </div>
  );
};

export default NflHomePage;