const { Sequelize, DataTypes } = require('sequelize');

// Initialize Sequelize with your database connection
const sequelize = new Sequelize('nfl_db', 'charlie', 'password1', {
  host: 'database',
  dialect: 'mysql'
});

// Export the sequelize instance and DataTypes for use in model definitions
module.exports = { sequelize, DataTypes };