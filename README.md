# 🎓 MarquisTeacher Academy — Backend API

**Author:** Marquis Williams  
**Stack:** Node.js · Express · Firebase Firestore · Nodemailer · JWT  
**Deploy:** Render.com  

---

## 📁 Project Structure

```
marquis-backend/
├── server.js               ← Entry point
├── package.json
├── .env.example            ← Copy to .env and fill in your values
├── .gitignore
├── config/
│   ├── firebase.js         ← Firebase Admin SDK setup
│   └── email.js            ← Nodemailer email functions
├── middleware/
│   └── auth.js             ← JWT authentication middleware
└── routes/
    ├── auth.js             ← Signup, Login, Get current user
    ├── exam.js             ← Submit result, Leaderboard, Stats
    └── contact.js          ← Contact form submissions
```

---

## ⚙️ API Endpoints

| Method | Route | Auth | Description |
|--------|-------|------|-------------|
| POST | `/api/auth/signup` | No | Create a new account |
| POST | `/api/auth/login` | No | Login and get JWT token |
| GET | `/api/auth/me` | Yes | Get current user profile |
| POST | `/api/exam/result` | No | Submit an exam result |
| GET | `/api/exam/board` | No | Get the leaderboard |
| GET | `/api/exam/board/stats` | No | Get board statistics |
| POST | `/api/contact` | No | Submit the contact form |
| GET | `/api/contact` | Admin | Get all contact submissions |
| GET | `/health` | No | Server health check |

---

## 🚀 Local Setup

### 1. Clone and install
```bash
git clone https://github.com/YOUR_USERNAME/marquis-backend.git
cd marquis-backend
npm install
```

### 2. Set up Firebase
1. Go to [Firebase Console](https://console.firebase.google.com)
2. Create a new project — name it `marquisteacher-academy`
3. Go to **Firestore Database** → Create database → Start in production mode
4. Go to **Project Settings** → **Service Accounts**
5. Click **Generate New Private Key** — save the JSON file
6. Copy the values into your `.env` file

### 3. Set up Gmail App Password
1. Go to your Google Account → **Security**
2. Enable **2-Step Verification** if not already on
3. Go to **App Passwords** → Select app: Mail → Generate
4. Copy the 16-character password into your `.env` file

### 4. Configure environment
```bash
cp .env.example .env
# Fill in all values in .env
```

### 5. Run locally
```bash
npm run dev
# Server starts at http://localhost:3000
```

---

## 🌐 Deploy to Render.com

1. Push this folder to a **new GitHub repo** (e.g. `marquis-backend`)
2. Go to [render.com](https://render.com) → Sign up free
3. Click **New** → **Web Service**
4. Connect your GitHub repo
5. Configure:
   - **Build Command:** `npm install`
   - **Start Command:** `npm start`
   - **Environment:** Node
6. Add all your `.env` variables under **Environment Variables**
7. Click **Deploy** — your API will be live at `https://your-app.onrender.com`

---

## 🔗 Connecting Frontend to Backend

Once deployed, update your `script.js` on the frontend:

```javascript
// Add this near the top of script.js
var API_URL = 'https://your-app.onrender.com';

// When exam result is saved, also POST to backend:
async function saveResultToServer(entry) {
  try {
    await fetch(API_URL + '/api/exam/result', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(entry)
    });
  } catch(e) {
    console.log('Could not sync to server:', e);
  }
}
```

---

## 🔒 Security Features

- **JWT Authentication** — tokens expire after 7 days
- **Password Hashing** — bcrypt with 12 salt rounds
- **Rate Limiting** — 100 req/15min globally, 10 req/15min on auth
- **CORS Protection** — only your frontend domain is allowed
- **Input Validation** — all routes validate required fields
- **Admin Protection** — sensitive routes require admin role

---

## 📜 License

MIT License — Copyright © 2025 Marquis Williams & MarquisTeacher Academy
