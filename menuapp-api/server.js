// Actual HTTP server

import app from './express.js';     // HTTP Requests run through this

// seperate with the port 3000
const port = process.env.PORT || 3004;

app.listen(port, (err) => {
    if (err) console.log(err);
    console.info(`Server started on port ${port}.`);
})