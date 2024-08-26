const mysql = require('mysql2/promise');

const pool = mysql.createPool({
  host: 'database',
  user: 'charlie',
  password: 'password1',
  database: 'nfl_db',
  waitForConnections: true,
  connectionLimit: 10,
  queueLimit: 0
});

module.exports = pool;