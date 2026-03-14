/* ============================================================
   MarquisTeacher Academy — Contact Routes
   POST /api/contact   — submit contact form
   GET  /api/contact   — get all submissions (protected, admin)
   ============================================================ */

const express = require('express');
const router  = express.Router();

const { db }               = require('../config/firebase');
const { sendContactEmail }  = require('../config/email');
const authMiddleware        = require('../middleware/auth');

// ── SUBMIT CONTACT FORM ───────────────────────────────────────
// POST /api/contact
// Body: { name, email, subject, message }
router.post('/', async (req, res) => {
  try {
    const { name, email, subject, message } = req.body;

    if (!name || !email || !subject || !message) {
      return res.status(400).json({ error: 'All fields are required.' });
    }

    // Basic email format check
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      return res.status(400).json({ error: 'Please enter a valid email address.' });
    }

    if (message.length < 10) {
      return res.status(400).json({ error: 'Message must be at least 10 characters.' });
    }

    // Save to Firestore
    await db.collection('contactSubmissions').add({
      name,
      email:     email.toLowerCase(),
      subject,
      message,
      createdAt: new Date().toISOString(),
      read:      false
    });

    // Send emails (forward to Marquis + auto-reply to sender)
    await sendContactEmail(name, email, subject, message);

    return res.status(201).json({
      message: 'Message sent successfully! We will get back to you within 24 hours.'
    });

  } catch (err) {
    console.error('Contact form error:', err);
    return res.status(500).json({ error: 'Could not send message. Please try again.' });
  }
});

// ── GET ALL SUBMISSIONS (admin only) ─────────────────────────
// GET /api/contact  (protected)
router.get('/', authMiddleware, async (req, res) => {
  try {
    // Only allow admin role
    if (req.user.role !== 'admin') {
      return res.status(403).json({ error: 'Admin access required.' });
    }

    const snapshot = await db.collection('contactSubmissions')
      .orderBy('createdAt', 'desc')
      .limit(100)
      .get();

    const submissions = snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
    return res.json({ submissions, count: submissions.length });

  } catch (err) {
    console.error('Get contacts error:', err);
    return res.status(500).json({ error: 'Could not fetch submissions.' });
  }
});

module.exports = router;
