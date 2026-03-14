/* ============================================================
   MarquisTeacher Academy — Exam Board Routes
   POST /api/exam/result      — submit a result
   GET  /api/exam/board       — get leaderboard
   GET  /api/exam/board/stats — get board statistics
   ============================================================ */

const express = require('express');
const router  = express.Router();

const { db }                 = require('../config/firebase');
const { sendExamResultEmail } = require('../config/email');
const authMiddleware         = require('../middleware/auth');

// CEFR points scale
const LEVEL_POINTS = { A1:10, A2:20, B1:40, B2:60, C1:80, C2:100 };

// ── SUBMIT EXAM RESULT ────────────────────────────────────────
// POST /api/exam/result
// Body: { name, email (optional), resultCode, selfLevel, score, maxScore }
router.post('/result', async (req, res) => {
  try {
    const { name, email, resultCode, resultName, selfLevel, score, maxScore } = req.body;

    if (!name || !resultCode || !selfLevel) {
      return res.status(400).json({ error: 'Name, result and self-assessed level are required.' });
    }

    const points = LEVEL_POINTS[resultCode] || 0;

    const entry = {
      name,
      email:      email || null,
      resultCode,
      resultName: resultName || resultCode,
      selfLevel,
      points,
      score:      score || 0,
      maxScore:   maxScore || 0,
      createdAt:  new Date().toISOString(),
      ts:         Date.now()
    };

    // Save to Firestore
    const docRef = await db.collection('examBoard').add(entry);

    // Send result email if email provided (non-blocking)
    if (email) {
      sendExamResultEmail(email, name, resultCode, resultName, points, selfLevel)
        .catch(err => console.error('Result email failed:', err));
    }

    return res.status(201).json({
      message: 'Result saved successfully!',
      id:      docRef.id,
      entry
    });

  } catch (err) {
    console.error('Submit result error:', err);
    return res.status(500).json({ error: 'Could not save result. Please try again.' });
  }
});

// ── GET LEADERBOARD ───────────────────────────────────────────
// GET /api/exam/board?limit=50
router.get('/board', async (req, res) => {
  try {
    const limit    = Math.min(parseInt(req.query.limit) || 50, 100);
    const snapshot = await db.collection('examBoard')
      .orderBy('points', 'desc')
      .orderBy('score', 'desc')
      .limit(limit)
      .get();

    const board = snapshot.docs.map(doc => ({
      id: doc.id,
      ...doc.data(),
      email: undefined // never expose emails publicly
    }));

    return res.json({ board, count: board.length });

  } catch (err) {
    console.error('Get board error:', err);
    return res.status(500).json({ error: 'Could not fetch leaderboard.' });
  }
});

// ── GET BOARD STATS ───────────────────────────────────────────
// GET /api/exam/board/stats
router.get('/board/stats', async (req, res) => {
  try {
    const snapshot = await db.collection('examBoard').get();
    const entries  = snapshot.docs.map(doc => doc.data());

    if (entries.length === 0) {
      return res.json({ total:0, avgPoints:0, topLevel:null, levelCounts:{} });
    }

    const total     = entries.length;
    const avgPoints = Math.round(entries.reduce((s,e) => s + (e.points||0), 0) / total);

    const levelCounts = {};
    entries.forEach(e => {
      levelCounts[e.resultCode] = (levelCounts[e.resultCode] || 0) + 1;
    });
    const topLevel = Object.keys(levelCounts).reduce((a,b) =>
      levelCounts[a] > levelCounts[b] ? a : b
    );

    return res.json({ total, avgPoints, topLevel, levelCounts });

  } catch (err) {
    console.error('Board stats error:', err);
    return res.status(500).json({ error: 'Could not fetch stats.' });
  }
});

module.exports = router;
