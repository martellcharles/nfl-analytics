const { sequelize, DataTypes } = require('./sequelize-setup');
const { Game } = require('./player-game');

const TeamStats = sequelize.define('TeamStats', {
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
    type: DataTypes.INTEGER,
    allowNull: true
  },
  passing_att: {
    type: DataTypes.INTEGER,
    allowNull: true
  },
  passing_cmp_prc: {
    type: DataTypes.FLOAT,
    allowNull: true
  },
  passing_yds: {
    type: DataTypes.INTEGER,
    allowNull: true
  },
  passing_tds: {
    type: DataTypes.INTEGER,
    allowNull: true
  },
  passing_int: {
    type: DataTypes.INTEGER,
    allowNull: true
  },
  passing_rate: {
    type: DataTypes.FLOAT,
    allowNull: true
  },
  passing_sacks: {
    type: DataTypes.INTEGER,
    allowNull: true
  },
  passing_sack_yds_lost: {
    type: DataTypes.INTEGER,
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
    type: DataTypes.INTEGER,
    allowNull: true
  },
  rushing_yds: {
    type: DataTypes.INTEGER,
    allowNull: true
  },
  rushing_yds_att: {
    type: DataTypes.FLOAT,
    allowNull: true
  },
  rushing_tds: {
    type: DataTypes.INTEGER,
    allowNull: true
  },
  scoring_tds: {
    type: DataTypes.INTEGER,
    allowNull: true
  },
  scoring_pts: {
    type: DataTypes.INTEGER,
    allowNull: true
  },
  punts: {
    type: DataTypes.INTEGER,
    allowNull: true
  },
  punt_yds: {
    type: DataTypes.INTEGER,
    allowNull: true
  },
  third_down_conv: {
    type: DataTypes.INTEGER,
    allowNull: true
  },
  third_down_att: {
    type: DataTypes.INTEGER,
    allowNull: true
  },
  fourth_down_conv: {
    type: DataTypes.INTEGER,
    allowNull: true
  },
  fourth_down_att: {
    type: DataTypes.INTEGER,
    allowNull: true
  }
}, {
  tableName: 'team_stats',
  timestamps: false
});

// Define association
Game.hasMany(TeamStats, { foreignKey: 'game_id' });
TeamStats.belongsTo(Game, { foreignKey: 'game_id' });

module.exports = TeamStats;