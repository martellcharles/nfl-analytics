const { sequelize, DataTypes } = require('./sequelize-setup');
const { Player } = require('./player-game');

const SeasonStats = sequelize.define('SeasonStats', {
  player_id: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    references: {
      model: Player,
      key: 'player_id'
    }
  },
  szn: {
    type: DataTypes.INTEGER,
    primaryKey: true
  },
  player_name: {
    type: DataTypes.STRING,
    allowNull: false
  },
  team: {
    type: DataTypes.STRING,
    allowNull: false
  },
  games_played: {
    type: DataTypes.INTEGER,
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
  passing_adj_yds_att: {
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
  receiving_rec: {
    type: DataTypes.INTEGER,
    allowNull: true
  },
  receiving_yds: {
    type: DataTypes.INTEGER,
    allowNull: true
  },
  receiving_yds_rec: {
    type: DataTypes.FLOAT,
    allowNull: true
  },
  receiving_tds: {
    type: DataTypes.INTEGER,
    allowNull: true
  },
  receiving_tgts: {
    type: DataTypes.INTEGER,
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
    type: DataTypes.INTEGER,
    allowNull: true
  },
  fumbles_fl: {
    type: DataTypes.INTEGER,
    allowNull: true
  }
}, {
  tableName: 'season_stats',
  timestamps: false
});


Player.hasMany(SeasonStats, { foreignKey: 'player_id' });
SeasonStats.belongsTo(Player, { foreignKey: 'player_id' });

module.exports = { SeasonStats };