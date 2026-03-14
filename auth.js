/* ============================================================
   MarquisTeacher Academy — Auth Routes
   POST /api/auth/signup
   POST /api/auth/login
   GET  /api/auth/me
   ============================================================ */

const express  = require('express');
const bcrypt   = require('bcryptjs');
const jwt      = require('jsonwebtoken');
const router   = express.Router();

const { db }              = require('../config/firebase');
const { sendWelcomeEmail } = require('../config/email');
const authMiddleware      = require('../middleware/auth');

// ── SIGNUP ────────────────────────────────────────────────────
// POST /api/auth/signup
// Body: { name, email, password }
router.post('/signup', async (req, res) => {
  try {
    const { name, email, password } = req.body;

    // Validate fields
    if (!name || !email || !password) {
      return res.status(400).json({ error: 'Name, email and password are required.' });
    }
    if (password.length < 8) {
      return res.status(400).json({ error: 'Password must be at least 8 characters.' });
    }

    // Check if email already exists
    const existing = await db.collection('users').where('email', '==', email.toLowerCase()).get();
    if (!existing.empty) {
      return res.status(409).json({ error: 'An account with this email already exists.' });
    }

    // Hash password
    const hashedPassword = await bcrypt.hash(password, 12);

    // Save user to Firestore
    const userRef = await db.collection('users').add({
      name,
      email:     email.toLowerCase(),
      password:  hashedPassword,
      createdAt: new Date().toISOString(),
      role:      'student'
    });

    // Generate JWT
    const token = jwt.sign(
      { uid: userRef.id, email: email.toLowerCase(), name, role: 'student' },
      process.env.JWT_SECRET,
      { expiresIn: process.env.JWT_EXPIRES_IN || '7d' }
    );

    // Send welcome email (non-blocking)
    sendWelcomeEmail(email, name).catch(err => console.error('Welcome email failed:', err));

    return res.status(201).json({
      message: 'Account created successfully!',
      token,
      user: { uid: userRef.id, name, email: email.toLowerCase(), role: 'student' }
    });

  } catch (err) {
    console.error('Signup error:', err);
    return res.status(500).json({ error: 'Something went wrong. Please try again.' });
  }
});

// ── LOGIN ─────────────────────────────────────────────────────
// POST /api/auth/login
// Body: { email, password }
router.post('/login', async (req, res) => {
  try {
    const { email, password } = req.body;

    if (!email || !password) {
      return res.status(400).json({ error: 'Email and password are required.' });
    }

    // Find user
    const snapshot = await db.collection('users').where('email', '==', email.toLowerCase()).get();
    if (snapshot.empty) {
      return res.status(401).json({ error: 'Invalid email or password.' });
    }

    const userDoc  = snapshot.docs[0];
    const userData = userDoc.data();

    // Check password
    const isValid = await bcrypt.compare(password, userData.password);
    if (!isValid) {
      return res.status(401).json({ error: 'Invalid email or password.' });
    }

    // Generate JWT
    const token = jwt.sign(
      { uid: userDoc.id, email: userData.email, name: userData.name, role: userData.role },
      process.env.JWT_SECRET,
      { expiresIn: process.env.JWT_EXPIRES_IN || '7d' }
    );

    return res.json({
      message: 'Login successful!',
      token,
      user: { uid: userDoc.id, name: userData.name, email: userData.email, role: userData.role }
    });

  } catch (err) {
    console.error('Login error:', err);
    return res.status(500).json({ error: 'Something went wrong. Please try again.' });
  }
});

// ── GET CURRENT USER ──────────────────────────────────────────
// GET /api/auth/me  (protected)
router.get('/me', authMiddleware, async (req, res) => {
  try {
    const userDoc = await db.collection('users').doc(req.user.uid).get();
    if (!userDoc.exists) {
      return res.status(404).json({ error: 'User not found.' });
    }
    const { password, ...safeData } = userDoc.data();
    return res.json({ uid: userDoc.id, ...safeData });
  } catch (err) {
    console.error('Get user error:', err);
    return res.status(500).json({ error: 'Something went wrong.' });
  }
});

module.exports = router;
