const express = require('express');
const cors = require('cors');
const app = express();
const seasonStatRoutes = require('./routes/season-stats')

app.use(cors());
app.use(express.json());
app.use('/api/season-stats', seasonStatRoutes);

app.use((req, res, next) => {
    console.log(`[Server] Received ${req.method} request to ${req.url}`);
    next();
});

// global error handler
app.use((err, req, res, next) => {
    console.error('[Server] Error:', err);
    res.status(500).send('Internal Server Error');
});

module.exports = app;