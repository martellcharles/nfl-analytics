const { sequelize, DataTypes } = require('./sequelize-setup');
const { Player, Game } = require('./player-game');

// CareerAvgStats Model
const CareerAvgStats = sequelize.define('CareerAvgStats', {
  game_id: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    references: {
      model: Game,
      key: 'game_id'
    }
  },
  szn: {
    type: DataTypes.INTEGER,
    allowNull: false
  },
  date: {
    type: DataTypes.DATE,
    allowNull: false
  },
  player_id: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    references: {
      model: Player,
      key: 'player_id'
    }
  },
  team: {
    type: DataTypes.STRING,
    allowNull: false
  },
  passing_cmp: {
    type: DataTypes.FLOAT,
    allowNull: true
  },
  passing_att: {
    type: DataTypes.FLOAT,
    allowNull: true
  },
  passing_cmp_prc: {
    type: DataTypes.FLOAT,
    allowNull: true
  },
  passing_yds: {
    type: DataTypes.FLOAT,
    allowNull: true
  },
  passing_tds: {
    type: DataTypes.FLOAT,
    allowNull: true
  },
  passing_int: {
    type: DataTypes.FLOAT,
    allowNull: true
  },
  passing_rate: {
    type: DataTypes.FLOAT,
    allowNull: true
  },
  passing_sacks: {
    type: DataTypes.FLOAT,
    allowNull: true
  },
  passing_sack_yds_lost: {
    type: DataTypes.FLOAT,
    allowNull: true
  },
  passing_yds_att: {
    type: DataTypes.FLOAT,
    allowNull: true
  },
  passing_adj_yds_att: {
    type: DataTypes.FLOAT,
    allowNull: true
  },
  rushing_att: {
    type: DataTypes.FLOAT,
    allowNull: true
  },
  rushing_yds: {
    type: DataTypes.FLOAT,
    allowNull: true
  },
  rushing_yds_att: {
    type: DataTypes.FLOAT,
    allowNull: true
  },
  rushing_tds: {
    type: DataTypes.FLOAT,
    allowNull: true
  },
  scoring_tds: {
    type: DataTypes.FLOAT,
    allowNull: true
  },
  scoring_pts: {
    type: DataTypes.FLOAT,
    allowNull: true
  },
  receiving_rec: {
    type: DataTypes.FLOAT,
    allowNull: true
  },
  receiving_yds: {
    type: DataTypes.FLOAT,
    allowNull: true
  },
  receiving_yds_rec: {
    type: DataTypes.FLOAT,
    allowNull: true
  },
  receiving_tds: {
    type: DataTypes.FLOAT,
    allowNull: true
  },
  receiving_tgts: {
    type: DataTypes.FLOAT,
    allowNull: true
  },
  receiving_catch_prc: {
    type: DataTypes.FLOAT,
    allowNull: true
  },
  receiving_yds_tgt: {
    type: DataTypes.FLOAT,
    allowNull: true
  },
  fumbles_fmb: {
    type: DataTypes.FLOAT,
    allowNull: true
  },
  fumbles_fl: {
    type: DataTypes.FLOAT,
    allowNull: true
  }
}, {
  tableName: 'career_avg_stats',
  timestamps: false
});

// SeasonAvgStats Model
const SeasonAvgStats = sequelize.define('SeasonAvgStats', {
  game_id: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    references: {
      model: Game,
      key: 'game_id'
    }
  },
  szn: {
    type: DataTypes.INTEGER,
    allowNull: false
  },
  date: {
    type: DataTypes.DATE,
    allowNull: false
  },
  player_id: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    references: {
      model: Player,
      key: 'player_id'
    }
  },
  team: {
    type: DataTypes.STRING,
    allowNull: false
  },
  passing_cmp: {
    type: DataTypes.FLOAT,
    allowNull: true
  },
  passing_att: {
    type: DataTypes.FLOAT,
    allowNull: true
  },
  passing_cmp_prc: {
    type: DataTypes.FLOAT,
    allowNull: true
  },
  passing_yds: {
    type: DataTypes.FLOAT,
    allowNull: true
  },
  passing_tds: {
    type: DataTypes.FLOAT,
    allowNull: true
  },
  passing_int: {
    type: DataTypes.FLOAT,
    allowNull: true
  },
  passing_rate: {
    type: DataTypes.FLOAT,
    allowNull: true
  },
  passing_sacks: {
    type: DataTypes.FLOAT,
    allowNull: true
  },
  passing_sack_yds_lost: {
    type: DataTypes.FLOAT,
    allowNull: true
  },
  passing_yds_att: {
    type: DataTypes.FLOAT,
    allowNull: true
  },
  passing_adj_yds_att: {
    type: DataTypes.FLOAT,
    allowNull: true
  },
  rushing_att: {
    type: DataTypes.FLOAT,
    allowNull: true
  },
  rushing_yds: {
    type: DataTypes.FLOAT,
    allowNull: true
  },
  rushing_yds_att: {
    type: DataTypes.FLOAT,
    allowNull: true
  },
  rushing_tds: {
    type: DataTypes.FLOAT,
    allowNull: true
  },
  scoring_tds: {
    type: DataTypes.FLOAT,
    allowNull: true
  },
  scoring_pts: {
    type: DataTypes.FLOAT,
    allowNull: true
  },
  receiving_rec: {
    type: DataTypes.FLOAT,
    allowNull: true
  },
  receiving_yds: {
    type: DataTypes.FLOAT,
    allowNull: true
  },
  receiving_yds_rec: {
    type: DataTypes.FLOAT,
    allowNull: true
  },
  receiving_tds: {
    type: DataTypes.FLOAT,
    allowNull: true
  },
  receiving_tgts: {
    type: DataTypes.FLOAT,
    allowNull: true
  },
  receiving_catch_prc: {
    type: DataTypes.FLOAT,
    allowNull: true
  },
  receiving_yds_tgt: {
    type: DataTypes.FLOAT,
    allowNull: true
  },
  fumbles_fmb: {
    type: DataTypes.FLOAT,
    allowNull: true
  },
  fumbles_fl: {
    type: DataTypes.FLOAT,
    allowNull: true
  }
}, {
  tableName: 'season_avg_stats',
  timestamps: false
});

// TeamAvgStats Model
const TeamAvgStats = sequelize.define('TeamAvgStats', {
  game_id: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    references: {
      model: Game,
      key: 'game_id'
    }
  },
  szn: {
    type: DataTypes.INTEGER,
    allowNull: false
  },
  date: {
    type: DataTypes.DATE,
    allowNull: false
  },
  team: {
    type: DataTypes.STRING,
    primaryKey: true,
    allowNull: false
  },
  passing_cmp: {
    type: DataTypes.FLOAT,
    allowNull: true
  },
  passing_att: {
    type: DataTypes.FLOAT,
    allowNull: true
  },
  passing_cmp_prc: {
    type: DataTypes.FLOAT,
    allowNull: true
  },
  passing_yds: {
    type: DataTypes.FLOAT,
    allowNull: true
  },
  passing_tds: {
    type: DataTypes.FLOAT,
    allowNull: true
  },
  passing_int: {
    type: DataTypes.FLOAT,
    allowNull: true
  },
  passing_rate: {
    type: DataTypes.FLOAT,
    allowNull: true
  },
  passing_sacks: {
    type: DataTypes.FLOAT,
    allowNull: true
  },
  passing_sack_yds_lost: {
    type: DataTypes.FLOAT,
    allowNull: true
  },
  passing_yds_att: {
    type: DataTypes.FLOAT,
    allowNull: true
  },
  passing_net_yds_att: {
    type: DataTypes.FLOAT,
    allowNull: true
  },
  rushing_att: {
    type: DataTypes.FLOAT,
    allowNull: true
  },
  rushing_yds: {
    type: DataTypes.FLOAT,
    allowNull: true
  },
  rushing_yds_att: {
    type: DataTypes.FLOAT,
    allowNull: true
  },
  rushing_tds: {
    type: DataTypes.FLOAT,
    allowNull: true
  },
  scoring_tds: {
    type: DataTypes.FLOAT,
    allowNull: true
  },
  scoring_pts: {
    type: DataTypes.FLOAT,
    allowNull: true
  },
  punts: {
    type: DataTypes.FLOAT,
    allowNull: true
  },
  punt_yds: {
    type: DataTypes.FLOAT,
    allowNull: true
  },
  third_down_conv: {
    type: DataTypes.FLOAT,
    allowNull: true
  },
  fourth_down_conv: {
    type: DataTypes.FLOAT,
    allowNull: true
  }
}, {
  tableName: 'team_avg_stats',
  timestamps: false
});

// Define associations
Player.hasMany(CareerAvgStats, { foreignKey: 'player_id' });
CareerAvgStats.belongsTo(Player, { foreignKey: 'player_id' });
Game.hasMany(CareerAvgStats, { foreignKey: 'game_id' });
CareerAvgStats.belongsTo(Game, { foreignKey: 'game_id' });

Player.hasMany(SeasonAvgStats, { foreignKey: 'player_id' });
SeasonAvgStats.belongsTo(Player, { foreignKey: 'player_id' });
Game.hasMany(SeasonAvgStats, { foreignKey: 'game_id' });
SeasonAvgStats.belongsTo(Game, { foreignKey: 'game_id' });

Game.hasMany(TeamAvgStats, { foreignKey: 'game_id' });
TeamAvgStats.belongsTo(Game, { foreignKey: 'game_id' });

module.exports = { CareerAvgStats, SeasonAvgStats, TeamAvgStats };