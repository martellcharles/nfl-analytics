import React, { useState, useEffect } from 'react';
import api from "../utils/api"
import styles from "./SeasonLeadersTable.module.css"

const SeasonLeadersTable = () => {
  const [leaderData, setLeaderData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchLeaders = async () => {
      try {
        const response = await api.get('/season-stats/season-leaders');
        console.log(response.data);
        setLeaderData(response.data);
        setIsLoading(false);
      } catch (e) {
        setError(e.message);
        setIsLoading(false);
      }
    };

    fetchLeaders();
  }, []);

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;
  if (!leaderData) return <div>No data available</div>;

  return (
    <div className={styles.container}>
      <h2 className={styles.title}>Season Leaders for {leaderData.season}</h2>
      <table className={styles.table}>
        <thead className={styles.tableHeader}>
          <tr>
            <th className={styles.tableHeaderCell}>Category</th>
            <th className={styles.tableHeaderCell}>Player</th>
            <th className={styles.tableHeaderCell}>Team</th>
            <th className={styles.tableHeaderCell}>Value</th>
          </tr>
        </thead>
        <tbody>
          {leaderData.leaders.map((leader, index) => (
            <tr key={index} className={styles.tableRow}>
              <td className={styles.tableCell}>{leader.category}</td>
              <td className={styles.tableCell}>{leader.playerName}</td>
              <td className={styles.tableCell}>{leader.team}</td>
              <td className={styles.tableCell}>{leader.value}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default SeasonLeadersTable;