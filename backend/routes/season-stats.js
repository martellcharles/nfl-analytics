const express = require('express');
const { SeasonStats } = require('../models/season-stats');
const { sequelize } = require('../models/sequelize-setup');

const router = express.Router();

router.get('/season-leaders', async (req, res) => {
  try {
    const year = 2023; // Hardcoded for 2023, but you could make this a query parameter

    const leaders = await SeasonStats.findAll({
      attributes: [
        'szn',
        [sequelize.fn('MAX', sequelize.col('passing_yds')), 'max_passing_yds'],
        [sequelize.fn('MAX', sequelize.col('rushing_yds')), 'max_rushing_yds'],
        [sequelize.fn('MAX', sequelize.col('receiving_yds')), 'max_receiving_yds'],
        [sequelize.fn('MAX', sequelize.col('scoring_tds')), 'max_scoring_tds'],
      ],
      where: {
        szn: year
      },
      raw: true
    });

    // Now fetch the player details for each leader
    const passingLeader = await SeasonStats.findOne({
      where: { szn: year, passing_yds: leaders[0].max_passing_yds },
      attributes: ['player_name', 'team', 'passing_yds'],
      raw: true
    });

    const rushingLeader = await SeasonStats.findOne({
      where: { szn: year, rushing_yds: leaders[0].max_rushing_yds },
      attributes: ['player_name', 'team', 'rushing_yds'],
      raw: true
    });

    const receivingLeader = await SeasonStats.findOne({
      where: { szn: year, receiving_yds: leaders[0].max_receiving_yds },
      attributes: ['player_name', 'team', 'receiving_yds'],
      raw: true
    });

    const scoringLeader = await SeasonStats.findOne({
      where: { szn: year, scoring_tds: leaders[0].max_scoring_tds },
      attributes: ['player_name', 'team', 'scoring_tds'],
      raw: true
    });

    const result = {
      season: year,
      leaders: [
        {
          category: "Passing Yards",
          playerName: passingLeader.player_name,
          team: passingLeader.team,
          value: passingLeader.passing_yds
        },
        {
          category: "Rushing Yards",
          playerName: rushingLeader.player_name,
          team: rushingLeader.team,
          value: rushingLeader.rushing_yds
        },
        {
          category: "Receiving Yards",
          playerName: receivingLeader.player_name,
          team: receivingLeader.team,
          value: receivingLeader.receiving_yds
        },
        {
          category: "Scoring Touchdowns",
          playerName: scoringLeader.player_name,
          team: scoringLeader.team,
          value: scoringLeader.scoring_tds
        }
      ]
    };

    res.json(result);
  } catch (error) {
    console.error('Error fetching season leaders:', error);
    res.status(500).json({ error: 'An error occurred while fetching season leaders' });
  }
});

module.exports = router;