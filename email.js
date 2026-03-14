/* ============================================================
   MarquisTeacher Academy — Email Utility (Nodemailer + Gmail)
   ============================================================ */

const nodemailer = require('nodemailer');

const transporter = nodemailer.createTransport({
  service: 'gmail',
  auth: {
    user: process.env.GMAIL_USER,
    pass: process.env.GMAIL_APP_PASSWORD
  }
});

// ── WELCOME EMAIL (sent to new user on signup) ────────────────
async function sendWelcomeEmail(toEmail, name) {
  await transporter.sendMail({
    from: '"MarquisTeacher Academy" <' + process.env.GMAIL_USER + '>',
    to:   toEmail,
    subject: '🎓 Welcome to MarquisTeacher Academy, ' + name + '!',
    html: `
      <div style="font-family:'Georgia',serif;max-width:600px;margin:auto;padding:40px 32px;background:#faf7f2;border-radius:12px;">
        <h1 style="font-size:2rem;color:#1a1a2e;margin-bottom:8px;">
          Welcome, <span style="color:#2ab3c8">${name}</span>!
        </h1>
        <p style="color:#6b7280;font-size:1rem;line-height:1.7;margin-bottom:24px;">
          You have successfully created your MarquisTeacher Academy account.
          We are thrilled to have you on this journey.
        </p>
        <div style="background:#1a1a2e;border-radius:8px;padding:24px;margin-bottom:24px;">
          <p style="color:#7dd8e8;font-size:0.85rem;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:8px;">Next Steps</p>
          <ul style="color:#e8eaf0;font-size:0.95rem;line-height:2;padding-left:20px;">
            <li>Take the English Level Assessment</li>
            <li>Check your rank on the Exam Board</li>
            <li>Book your free consultation</li>
          </ul>
        </div>
        <a href="${process.env.FRONTEND_URL}" 
           style="display:inline-block;background:#2ab3c8;color:white;padding:12px 28px;border-radius:4px;text-decoration:none;font-size:0.9rem;font-weight:500;">
          Visit MarquisTeacher Academy →
        </a>
        <p style="color:#9ca3af;font-size:0.8rem;margin-top:32px;border-top:1px solid #e5e7eb;padding-top:16px;">
          MarquisTeacher Academy · MarquisTeacher@gmail.com<br>
          © 2025 Marquis Williams & MarquisTeacher Academy
        </p>
      </div>
    `
  });
}

// ── EXAM RESULT EMAIL (sent after completing the quiz) ────────
async function sendExamResultEmail(toEmail, name, resultCode, resultName, points, selfLevel) {
  const matched = resultCode === selfLevel;
  const comparison = matched
    ? 'Your result matched your self-assessment perfectly!'
    : 'Your result was ' + resultCode + ' — use this as your roadmap to keep growing!';

  await transporter.sendMail({
    from: '"MarquisTeacher Academy" <' + process.env.GMAIL_USER + '>',
    to:   toEmail,
    subject: '📊 Your MarquisTeacher Exam Result — ' + resultCode + ' ' + resultName,
    html: `
      <div style="font-family:'Georgia',serif;max-width:600px;margin:auto;padding:40px 32px;background:#faf7f2;border-radius:12px;">
        <h1 style="font-size:1.8rem;color:#1a1a2e;margin-bottom:8px;">Your Exam Result</h1>
        <p style="color:#6b7280;margin-bottom:24px;">Well done on completing the MarquisTeacher English Assessment, ${name}!</p>
        <div style="background:#1a1a2e;border-radius:8px;padding:28px;text-align:center;margin-bottom:24px;">
          <div style="font-size:3rem;font-weight:900;color:#2ab3c8;line-height:1;">${resultCode}</div>
          <div style="color:#e8eaf0;font-size:1rem;margin-top:8px;">${resultName}</div>
          <div style="color:#7dd8e8;font-size:0.85rem;margin-top:4px;">${points} points on the HDX Scale</div>
        </div>
        <p style="color:#374151;font-size:0.95rem;line-height:1.7;margin-bottom:24px;">${comparison}</p>
        <a href="mailto:${process.env.GMAIL_USER}?subject=Free Consultation — ${resultCode} Level"
           style="display:inline-block;background:#2ab3c8;color:white;padding:12px 28px;border-radius:4px;text-decoration:none;font-size:0.9rem;font-weight:500;">
          Book a Free Consultation →
        </a>
        <p style="color:#9ca3af;font-size:0.8rem;margin-top:32px;border-top:1px solid #e5e7eb;padding-top:16px;">
          MarquisTeacher Academy · MarquisTeacher@gmail.com<br>
          © 2025 Marquis Williams & MarquisTeacher Academy
        </p>
      </div>
    `
  });
}

// ── CONTACT FORM EMAIL (forwarded to Marquis) ─────────────────
async function sendContactEmail(senderName, senderEmail, subject, message) {
  await transporter.sendMail({
    from: '"MarquisTeacher Academy" <' + process.env.GMAIL_USER + '>',
    to:   process.env.GMAIL_USER,
    replyTo: senderEmail,
    subject: '📬 New Contact: ' + subject,
    html: `
      <div style="font-family:Arial,sans-serif;max-width:600px;margin:auto;padding:32px;background:#f9fafb;border-radius:8px;">
        <h2 style="color:#1a1a2e;">New Message from MarquisTeacher Academy</h2>
        <table style="width:100%;border-collapse:collapse;margin-top:16px;">
          <tr><td style="padding:8px;color:#6b7280;width:120px;">Name</td><td style="padding:8px;font-weight:500;">${senderName}</td></tr>
          <tr style="background:#fff;"><td style="padding:8px;color:#6b7280;">Email</td><td style="padding:8px;"><a href="mailto:${senderEmail}">${senderEmail}</a></td></tr>
          <tr><td style="padding:8px;color:#6b7280;">Subject</td><td style="padding:8px;">${subject}</td></tr>
        </table>
        <div style="background:#fff;border-radius:6px;padding:16px;margin-top:16px;border-left:3px solid #2ab3c8;">
          <p style="color:#374151;line-height:1.7;margin:0;">${message.replace(/\n/g, '<br>')}</p>
        </div>
      </div>
    `
  });

  // Auto-reply to sender
  await transporter.sendMail({
    from: '"MarquisTeacher Academy" <' + process.env.GMAIL_USER + '>',
    to:   senderEmail,
    subject: '✅ We received your message — MarquisTeacher Academy',
    html: `
      <div style="font-family:'Georgia',serif;max-width:600px;margin:auto;padding:40px 32px;background:#faf7f2;border-radius:12px;">
        <h1 style="font-size:1.6rem;color:#1a1a2e;">Thanks for reaching out, ${senderName}!</h1>
        <p style="color:#6b7280;line-height:1.7;margin:16px 0;">
          We have received your message and will get back to you within 24 hours.
        </p>
        <p style="color:#9ca3af;font-size:0.8rem;margin-top:32px;border-top:1px solid #e5e7eb;padding-top:16px;">
          MarquisTeacher Academy · MarquisTeacher@gmail.com<br>
          © 2025 Marquis Williams & MarquisTeacher Academy
        </p>
      </div>
    `
  });
}

module.exports = { sendWelcomeEmail, sendExamResultEmail, sendContactEmail };
