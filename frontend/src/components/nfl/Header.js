import React from 'react';
import { Link } from 'react-router-dom';
import styles from './Header.module.css';

const Header = () => {

    return (
        <header className={styles.header}>
        <nav className={styles.nav}>
        <span className={styles.greeting}>Hello</span>
            <div className={styles.navLinks}>
                <Link to="/nfl/teams" className={styles.navLink}>Teams</Link>
                <Link to="/nfl/players" className={styles.navLink}>Players</Link>
                <Link to="/nfl/season-leaders" className={styles.navLink}>Season Leaders</Link>
                <Link to="/nfl/other" className={styles.navLink}>Other</Link>
            </div>
        </nav>
        </header>
    );
};

export default Header;