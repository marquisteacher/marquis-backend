/* ============================================================
   MarquisTeacher Academy — Express Server
   ============================================================ */

require('dotenv').config();

const express    = require('express');
const cors       = require('cors');
const rateLimit  = require('express-rate-limit');

const authRoutes    = require('./routes/auth');
const examRoutes    = require('./routes/exam');
const contactRoutes = require('./routes/contact');

const app  = express();
app.set('trust proxy', 1);
const PORT = process.env.PORT || 3000;

// ── MIDDLEWARE ────────────────────────────────────────────────

// CORS — only allow your frontend
app.use(cors({
  origin: [
    'https://marquisteacher.github.io',
    'https://marquisteacher.github.io/marquisteacher-academy',
    'http://localhost:5500',
    'http://127.0.0.1:5500',
    process.env.FRONTEND_URL
  ],
  methods: ['GET','POST','PUT','DELETE','OPTIONS'],
  credentials: true
}));

// Parse JSON
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Rate limiting — protect against abuse
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max:      100,             // max 100 requests per window
  message:  { error: 'Too many requests. Please try again in 15 minutes.' }
});
app.use('/api/', limiter);

// Stricter limit on auth routes
const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max:      10,
  message:  { error: 'Too many login attempts. Please try again in 15 minutes.' }
});
app.use('/api/auth/', authLimiter);

// ── ROUTES ────────────────────────────────────────────────────
app.use('/api/auth',    authRoutes);
app.use('/api/exam',    examRoutes);
app.use('/api/contact', contactRoutes);

// ── HEALTH CHECK ──────────────────────────────────────────────
app.get('/health', (req, res) => {
  res.json({
    status:  'OK',
    service: 'MarquisTeacher Academy API',
    time:    new Date().toISOString()
  });
});

// ── ROOT ──────────────────────────────────────────────────────
app.get('/', (req, res) => {
  res.json({
    message: '🎓 MarquisTeacher Academy API',
    version: '1.0.0',
    author:  'Marquis Williams',
    routes: {
      auth:    '/api/auth    — signup, login, me',
      exam:    '/api/exam    — submit result, leaderboard, stats',
      contact: '/api/contact — contact form'
    }
  });
});

// ── 404 HANDLER ───────────────────────────────────────────────
app.use((req, res) => {
  res.status(404).json({ error: 'Route not found.' });
});

// ── ERROR HANDLER ─────────────────────────────────────────────
app.use((err, req, res, next) => {
  console.error('Unhandled error:', err);
  res.status(500).json({ error: 'Internal server error.' });
});

// ── START ─────────────────────────────────────────────────────
app.listen(PORT,'0.0.0.0', () => {
  console.log('');
  console.log('  🎓 MarquisTeacher Academy API');
  console.log('  ─────────────────────────────');
  console.log('  Server running on port ' + PORT);
  console.log('  Health: http://localhost:' + PORT + '/health');
  console.log('');
});

module.exports = app;
