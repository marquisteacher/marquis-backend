# ⚙️ MarquisTeacher Academy — Backend API

> *The engine powering the MarquisTeacher ecosystem.*

A secure, production-ready REST API built with Node.js and Express, connected to Firebase Firestore — handling authentication, exam results, leaderboard data and contact submissions.

---

## 🌐 Live API

```
https://marquisteacher-backend.onrender.com
```

### Quick Health Check
```
https://marquisteacher-backend.onrender.com/health
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Runtime | Node.js v24+ |
| Framework | Express.js |
| Database | Firebase Firestore |
| Authentication | JWT (JSON Web Tokens) |
| Password Hashing | bcryptjs (12 salt rounds) |
| Email | Nodemailer + Gmail |
| Security | express-rate-limit · CORS |
| Hosting | Render.com (Free Tier) |

---

## 📁 Project Structure

```
marquisteacher-backend/
├── server.js               ← Entry point
├── package.json            ← Dependencies
├── .env.example            ← Environment template
├── .gitignore              ← Protects secrets
├── config/
│   ├── firebase.js         ← Firebase Admin SDK
│   └── email.js            ← Nodemailer email functions
├── middleware/
│   └── auth.js             ← JWT authentication middleware
└── routes/
    ├── auth.js             ← Signup · Login · Get user
    ├── exam.js             ← Results · Leaderboard · Stats
    └── contact.js          ← Contact form submissions
```

---

## 📡 API Endpoints

| Method | Route | Auth | Description |
|--------|-------|------|-------------|
| `POST` | `/api/auth/signup` | No | Create a new account |
| `POST` | `/api/auth/login` | No | Login and receive JWT token |
| `GET` | `/api/auth/me` | Yes | Get current user profile |
| `POST` | `/api/exam/result` | No | Submit an exam result |
| `GET` | `/api/exam/board` | No | Get the leaderboard |
| `GET` | `/api/exam/board/stats` | No | Get board statistics |
| `POST` | `/api/contact` | No | Submit contact form |
| `GET` | `/api/contact` | Admin | View all submissions |
| `GET` | `/health` | No | Server health check |

---

## 🔒 Security Features

```
✅ JWT Authentication      — tokens expire after 7 days
✅ Password Hashing        — bcrypt with 12 salt rounds
✅ Rate Limiting           — 100 req/15min globally
✅ Auth Rate Limiting      — 10 req/15min on auth routes
✅ CORS Protection         — only allowed origins accepted
✅ Input Validation        — all routes validate required fields
✅ Admin Protection        — sensitive routes require admin role
✅ Environment Variables   — all secrets in .env, never in code
```

---

## ⚙️ Local Setup

### Prerequisites
- Node.js v18+
- Firebase project
- Gmail account with App Password

### 1. Clone and install
```bash
git clone https://github.com/marquisteacher/marquisteacher-backend.git
cd marquisteacher-backend
npm install
```

### 2. Configure environment
```bash
cp .env.example .env
```

Fill in your `.env` file:
```env
PORT=3000
JWT_SECRET=your_generated_secret
JWT_EXPIRES_IN=7d
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_CLIENT_EMAIL=your-client-email
FIREBASE_PRIVATE_KEY="your-private-key"
GMAIL_USER=MarquisTeacher@gmail.com
GMAIL_APP_PASSWORD=your-app-password
FRONTEND_URL=https://marquisteacher.github.io
```

### 3. Generate JWT Secret
```bash
node -e "console.log(require('crypto').randomBytes(64).toString('hex'))"
```

### 4. Run locally
```bash
npm run dev
```

Server starts at `http://localhost:3000` ✅

---

## 🌐 Deploy to Render.com

1. Push repository to GitHub
2. Go to [render.com](https://render.com) → New Web Service
3. Connect your repository
4. Configure:
   - **Build Command:** `npm install`
   - **Start Command:** `npm start`
5. Add all environment variables
6. Deploy! 🚀

---

## 📧 Email Notifications

Three automated emails are sent:

| Trigger | Recipients | Content |
|---------|-----------|---------|
| New signup | Student | Welcome email with next steps |
| Exam complete | Student | Result, level, consultation CTA |
| Contact form | Marquis + Student | Message forward + auto-reply |

---

## 🔗 Connected Services

| Service | Purpose |
|---------|---------|
| [Academy Frontend](https://github.com/marquisteacher/marquisteacher-academy) | Landing page |
| [AI Tutor](https://github.com/marquisteacher/marquisteacher-tutor) | Tutoring app |
| Firebase Firestore | Data storage |
| Gmail | Email delivery |

---

## 📬 Contact

**Marquis Williams**
📧 MarquisTeacher@gmail.com

---

## 📜 License

MIT License — Copyright © 2025 Marquis Williams & MarquisTeacher Academy

See [LICENSE](./LICENSE) for full details.

---

> Built with 💙 by Marquis Williams · MarquisTeacher Academy · 2025
