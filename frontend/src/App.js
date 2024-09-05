import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import HomePage from './pages/HomePage'
import EplHomePage from './pages/epl/HomePage'
import MlbHomePage from './pages/mlb/HomePage'
import NbaHomePage from './pages/nba/HomePage'
import NflHomePage from './pages/nfl/HomePage'
import NflTeamsPage from './pages/nfl/TeamsPage'
import NflPlayersPage from './pages/nfl/PlayersPage'
import NflSeasonLeadersPage from './pages/nfl/SeasonLeadersPage'
import NhlHomePage from './pages/nhl/HomePage'

function App() {
    return (
        <Router>
            <div className="app-container">
                <Routes>
                    <Route path="/" element={<HomePage />} />
                    <Route path="/epl" element={<EplHomePage />} />
                    <Route path="/mlb" element={<MlbHomePage />} />
                    <Route path="/nba" element={<NbaHomePage />} />
                    <Route path="/nfl" element={<NflHomePage />} />
                    <Route path="/nfl/teams" element={<NflTeamsPage />} />
                    <Route path="/nfl/players" element={<NflPlayersPage />} />
                    <Route path="/nfl/season-leaders" element={<NflSeasonLeadersPage />} />
                    <Route path="/nhl" element={<NhlHomePage />} />
                </Routes>
            </div>
        </Router>
    );
  }
  
  export default App;