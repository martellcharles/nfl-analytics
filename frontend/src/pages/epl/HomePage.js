import React from 'react';
// import SeasonLeadersTable from '../../components/epl/SeasonLeadersTable';
import styles from './HomePage.module.css'


const EplHomePage = () => {

  return (
    <div className={styles.homePage}>
      <div className={styles.hero}>
        <h1>Welcome to the EPL analytics page</h1>
        <p>Discover the power of analytics here</p>
        <p>Coming soon!</p>
        {/* <SeasonLeadersTable /> */}
      </div>
    </div>
  );
};

export default EplHomePage;