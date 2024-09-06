import React from 'react';
import styles from './TeamsPage.module.css';
import Header from '../../components/nfl/Header';

const nflTeams = {
    AFC: {
      North: [
        { name: 'Baltimore Ravens', slug: 'baltimore-ravens' },
        { name: 'Cincinnati Bengals', slug: 'cincinnati-bengals' },
        { name: 'Cleveland Browns', slug: 'cleveland-browns' },
        { name: 'Pittsburgh Steelers', slug: 'pittsburgh-steelers' },
      ],
      South: [
        { name: 'Houston Texans', slug: 'houston-texans' },
        { name: 'Indianapolis Colts', slug: 'indianapolis-colts' },
        { name: 'Jacksonville Jaguars', slug: 'jacksonville-jaguars' },
        { name: 'Tennessee Titans', slug: 'tennessee-titans' },
      ],
      East: [
        { name: 'Buffalo Bills', slug: 'buffalo-bills' },
        { name: 'Miami Dolphins', slug: 'miami-dolphins' },
        { name: 'New England Patriots', slug: 'new-england-patriots' },
        { name: 'New York Jets', slug: 'new-york-jets' },
      ],
      West: [
        { name: 'Denver Broncos', slug: 'denver-broncos' },
        { name: 'Kansas City Chiefs', slug: 'kansas-city-chiefs' },
        { name: 'Las Vegas Raiders', slug: 'las-vegas-raiders' },
        { name: 'Los Angeles Chargers', slug: 'los-angeles-chargers' },
      ],
    },
    NFC: {
      North: [
        { name: 'Chicago Bears', slug: 'chicago-bears' },
        { name: 'Detroit Lions', slug: 'detroit-lions' },
        { name: 'Green Bay Packers', slug: 'green-bay-packers' },
        { name: 'Minnesota Vikings', slug: 'minnesota-vikings' },
      ],
      South: [
        { name: 'Atlanta Falcons', slug: 'atlanta-falcons' },
        { name: 'Carolina Panthers', slug: 'carolina-panthers' },
        { name: 'New Orleans Saints', slug: 'new-orleans-saints' },
        { name: 'Tampa Bay Buccaneers', slug: 'tampa-bay-buccaneers' },
      ],
      East: [
        { name: 'Dallas Cowboys', slug: 'dallas-cowboys' },
        { name: 'New York Giants', slug: 'new-york-giants' },
        { name: 'Philadelphia Eagles', slug: 'philadelphia-eagles' },
        { name: 'Washington Commanders', slug: 'washington-commanders' },
      ],
      West: [
        { name: 'Arizona Cardinals', slug: 'arizona-cardinals' },
        { name: 'Los Angeles Rams', slug: 'los-angeles-rams' },
        { name: 'San Francisco 49ers', slug: 'san-francisco-49ers' },
        { name: 'Seattle Seahawks', slug: 'seattle-seahawks' },
      ],
    },
  };

const TeamsPage = () => {

  return (
    <div className={styles.container}>
    <Header />
      {Object.entries(nflTeams).map(([conference, divisions]) => (
        <div key={conference} className={styles.conference}>
          <h2 className={styles.conferenceTitle}>{conference}</h2>
          <div className={styles.conferenceGrid}>
            {Object.entries(divisions).map(([division, teams]) => (
              <div key={division} className={styles.division}>
                <h3 className={styles.divisionTitle}>{division}</h3>
                <div className={styles.teamsGrid}>
                  {teams.map((team) => (
                    <a key={team.name} href={`/nfl/teams/${team.slug}`} className={styles.teamLink}>
                      <div className={styles.teamCard}>
                        <span className={styles.teamName}>{team.name}</span>
                      </div>
                    </a>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
};

export default TeamsPage;