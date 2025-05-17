// MongoDB connection via mongoose
import './db.js';

// Middleware from mode_modules/
import express from 'express';   // express
import cookieParser from 'cookie-parser';  // express uses to parse HTTP cookies in Request
import compression from 'compression';     // server can accept compressed file
import morgan from 'morgan';     // data logger to log responese and request in the console
import cors from 'cors';         // enables CORS for API from different domain, protocol, port access API

import router from './routes/api-router.js';

const app = express();

// Express middleware
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
// Request chain
app.use(cookieParser());
app.use(compression());
app.use(morgan('dev'));
app.use(cors());

// Routing
app.get('/', (req, res) => {
    res.send('Node.js Server is live!');
});

// Callback to any HTTP requests
app.use('/m1', router);
  
export default app;
