const { sequelize, DataTypes } = require('./sequelize-setup');

const Player = sequelize.define('Player', {
  player_id: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    unique: true,
    allowNull: false,
    autoIncrement: true
  },
  first_name: {
    type: DataTypes.STRING,
    allowNull: false
  },
  last_name: {
    type: DataTypes.STRING,
    allowNull: false
  },
  position: {
    type: DataTypes.STRING,
    allowNull: false
  },
  first_year: {
    type: DataTypes.INTEGER,
    allowNull: true
  },
  last_year: {
    type: DataTypes.INTEGER,
    allowNull: true
  }
}, {
  tableName: 'players',
  timestamps: false
});

const Game = sequelize.define('Game', {
  game_id: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    unique: true,
    allowNull: false,
    autoIncrement: true
  },
  szn: {
    type: DataTypes.INTEGER,
    allowNull: false
  },
  date: {
    type: DataTypes.DATE,
    allowNull: false
  },
  home_team: {
    type: DataTypes.STRING,
    allowNull: false
  },
  away_team: {
    type: DataTypes.STRING,
    allowNull: false
  },
  home_score: {
    type: DataTypes.INTEGER,
    allowNull: false
  },
  away_score: {
    type: DataTypes.INTEGER,
    allowNull: false
  },
  game_type: {
    type: DataTypes.STRING,
    allowNull: false
  }
}, {
  tableName: 'games',
  timestamps: false
});

module.exports = { Player, Game };