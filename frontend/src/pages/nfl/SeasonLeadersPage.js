import React from 'react';
import SeasonLeadersTable from '../../components/nfl/SeasonLeadersTable';
// import styles from './HomePage.module.css'


const SeasonLeadersPage = () => {

  return (
    <div>
      <div>
        <h1>NFL Season Leaders</h1>
        <SeasonLeadersTable />
      </div>
    </div>
  );
};

export default SeasonLeadersPage;