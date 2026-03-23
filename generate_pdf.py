"""
============================================================
MarquisTeacher Academy — Custom PDF Learning Plan Generator
Author: Marquis Williams
============================================================
Generates a personalised CEFR learning plan PDF based on
a student's exam results and skill breakdown scores.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table,
    TableStyle, HRFlowable, PageBreak
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate
import os
from datetime import datetime

# ── BRAND COLORS ─────────────────────────────────────────────
TEAL        = colors.HexColor('#2ab3c8')
TEAL_DARK   = colors.HexColor('#1a8fa2')
TEAL_LIGHT  = colors.HexColor('#7dd8e8')
INK         = colors.HexColor('#1a1a2e')
CREAM       = colors.HexColor('#faf7f2')
PAPER       = colors.HexColor('#f5f0e8')
GRAY        = colors.HexColor('#6b7280')
WHITE       = colors.white
GOLD        = colors.HexColor('#c9a84c')

LEVEL_COLORS = {
    'A1': colors.HexColor('#2ab3c8'),
    'A2': colors.HexColor('#27ae60'),
    'B1': colors.HexColor('#f39c12'),
    'B2': colors.HexColor('#e67e22'),
    'C1': colors.HexColor('#e74c3c'),
    'C2': colors.HexColor('#8e44ad'),
}

LEVEL_NAMES = {
    'A1': 'Beginner',
    'A2': 'Elementary',
    'B1': 'Intermediate',
    'B2': 'Upper-Intermediate',
    'C1': 'Advanced',
    'C2': 'Mastery',
}

NEXT_LEVEL = {
    'A1': 'A2', 'A2': 'B1', 'B1': 'B2',
    'B2': 'C1', 'C1': 'C2', 'C2': 'C2'
}

LEVEL_POINTS = {
    'A1': 10, 'A2': 20, 'B1': 40,
    'B2': 60, 'C1': 80, 'C2': 100
}

# ── LEARNING STRATEGIES PER SKILL ────────────────────────────
SKILL_STRATEGIES = {
    'Grammar': {
        'icon': '📐',
        'description': 'Grammar forms the backbone of clear communication.',
        'weak': [
            'Study one grammar rule per day — consistency beats cramming',
            'Use BBC Learning English Grammar exercises (free online)',
            'Keep a grammar journal — write 5 sentences using each new rule',
            'Practice conditionals and tenses with daily writing prompts',
            'Use Grammarly or LanguageTool to get instant feedback on writing',
        ],
        'strong': [
            'Challenge yourself with advanced structures — subjunctive, inversion',
            'Read academic or legal texts to see complex grammar in context',
            'Help others with grammar — teaching reinforces mastery',
            'Write formal essays and get feedback from MarquisTeacher',
        ]
    },
    'Vocabulary': {
        'icon': '📖',
        'description': 'A rich vocabulary unlocks precise and powerful expression.',
        'weak': [
            'Learn 5 new words every day using spaced repetition (Anki app)',
            'Read one English article daily — highlight unknown words',
            'Use words in sentences immediately after learning them',
            'Group words by theme: emotions, business, nature, technology',
            'Watch English films/series with subtitles — pause and note new words',
        ],
        'strong': [
            'Explore etymology — understanding word roots accelerates learning',
            'Read literary fiction to encounter sophisticated vocabulary',
            'Practice using advanced synonyms in everyday conversation',
            'Study collocations — words that naturally go together in English',
        ]
    },
    'Reading': {
        'icon': '📰',
        'description': 'Reading comprehension connects language to meaning and context.',
        'weak': [
            'Read short English articles daily — start with BBC News Simple English',
            'Practice identifying the main idea before reading details',
            'Learn to infer meaning from context — guess before checking dictionary',
            'Summarise what you read in 2-3 sentences after each article',
            'Use highlighting to identify key arguments and supporting details',
        ],
        'strong': [
            'Read complex texts: academic papers, opinion pieces, literature',
            'Practice critical reading — question the author\'s assumptions',
            'Read across genres: fiction, non-fiction, journalism, science',
            'Take notes while reading — develop analytical reading habits',
        ]
    },
    'Idioms': {
        'icon': '💬',
        'description': 'Idioms and expressions bring colour and naturalness to English.',
        'weak': [
            'Learn 3 idioms per week — use them in conversation immediately',
            'Group idioms by topic: work, relationships, time, money',
            'Watch English comedy shows — idioms appear naturally in dialogue',
            'Keep an idiom journal with meaning, example sentence and context',
            'Practice with a language partner — use new idioms in real conversation',
        ],
        'strong': [
            'Explore regional expressions — British vs American vs Australian English',
            'Study the history behind idioms — understanding origins aids memory',
            'Use idioms naturally in writing — essays, emails, creative writing',
            'Challenge yourself with proverbs and more complex figurative language',
        ]
    }
}

# ── 30-DAY ROADMAP PER LEVEL ──────────────────────────────────
ROADMAPS = {
    'A1': {
        'goal': 'Build your foundation — master everyday English basics',
        'weeks': [
            ('Week 1', 'Present simple, basic vocabulary (greetings, numbers, colours)'),
            ('Week 2', 'Common phrases, question formation, daily routines'),
            ('Week 3', 'Past simple, describing people and places'),
            ('Week 4', 'Future tense, simple conversations, review and practice'),
        ]
    },
    'A2': {
        'goal': 'Expand your range — communicate in familiar situations confidently',
        'weeks': [
            ('Week 1', 'Present perfect, comparatives and superlatives'),
            ('Week 2', 'Modal verbs (can, could, should), shopping and travel vocabulary'),
            ('Week 3', 'Conditionals (first conditional), expressing opinions'),
            ('Week 4', 'Reported speech basics, reading short texts, review'),
        ]
    },
    'B1': {
        'goal': 'Build fluency — handle most everyday situations with confidence',
        'weeks': [
            ('Week 1', 'Second conditional, passive voice, work and career vocabulary'),
            ('Week 2', 'Relative clauses, academic vocabulary, reading comprehension'),
            ('Week 3', 'Discourse markers, expressing complex opinions, idioms'),
            ('Week 4', 'Writing structured paragraphs, listening practice, review'),
        ]
    },
    'B2': {
        'goal': 'Refine your English — communicate effectively across a wide range of topics',
        'weeks': [
            ('Week 1', 'Advanced conditionals, subjunctive mood, formal vocabulary'),
            ('Week 2', 'Inversion, cleft sentences, academic reading and writing'),
            ('Week 3', 'Advanced idioms, register and tone, persuasive writing'),
            ('Week 4', 'Complex grammar structures, debate practice, review'),
        ]
    },
    'C1': {
        'goal': 'Achieve mastery — express yourself with precision and sophistication',
        'weeks': [
            ('Week 1', 'Nuanced vocabulary, advanced academic writing, rhetoric'),
            ('Week 2', 'Complex discourse, implicit meaning, literary analysis'),
            ('Week 3', 'Advanced idioms and collocations, professional communication'),
            ('Week 4', 'Stylistic writing, public speaking, comprehensive review'),
        ]
    },
    'C2': {
        'goal': 'Maintain and deepen your mastery — you have reached the pinnacle',
        'weeks': [
            ('Week 1', 'Explore specialised vocabulary in your field of interest'),
            ('Week 2', 'Read challenging literature and academic papers'),
            ('Week 3', 'Refine writing style — precision, elegance, persuasion'),
            ('Week 4', 'Mentor others, teach what you know, maintain excellence'),
        ]
    }
}

# ── DAILY STUDY PLAN ─────────────────────────────────────────
DAILY_PLANS = {
    'A1': [
        ('Morning (10 min)',   'Vocabulary flashcards — 5 new words'),
        ('Afternoon (15 min)', 'Grammar exercise — one rule per day'),
        ('Evening (10 min)',   'Write 3 sentences using today\'s words'),
        ('Weekend',            'Watch one English video with subtitles'),
    ],
    'A2': [
        ('Morning (10 min)',   'Vocabulary review + 5 new words'),
        ('Afternoon (20 min)', 'Reading comprehension — short article'),
        ('Evening (10 min)',   'Grammar practice and sentence writing'),
        ('Weekend',            'Conversation practice with language partner'),
    ],
    'B1': [
        ('Morning (15 min)',   'Read one English article — summarise in notes'),
        ('Afternoon (20 min)', 'Grammar and vocabulary exercises'),
        ('Evening (15 min)',   'Writing practice — structured paragraphs'),
        ('Weekend',            'AI tutor conversation session (15 minutes)'),
    ],
    'B2': [
        ('Morning (20 min)',   'Read complex text — identify argument structure'),
        ('Afternoon (20 min)', 'Advanced grammar and vocabulary work'),
        ('Evening (15 min)',   'Writing — essays, emails, formal texts'),
        ('Weekend',            'AI tutor debate and discussion session'),
    ],
    'C1': [
        ('Morning (20 min)',   'Read academic or literary text — critical analysis'),
        ('Afternoon (25 min)', 'Advanced writing practice — rhetoric and style'),
        ('Evening (15 min)',   'Vocabulary refinement — collocations and register'),
        ('Weekend',            'AI tutor advanced conversation and feedback'),
    ],
    'C2': [
        ('Morning (20 min)',   'Read challenging literature or academic papers'),
        ('Afternoon (25 min)', 'Write in your specialised field — essays or articles'),
        ('Evening (15 min)',   'Explore etymology, linguistics, advanced expression'),
        ('Weekend',            'Mentor others — teach and reinforce your mastery'),
    ],
}

# ── PAGE BACKGROUND ───────────────────────────────────────────
def add_page_background(canvas_obj, doc):
    canvas_obj.saveState()
    canvas_obj.setFillColor(CREAM)
    canvas_obj.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)

    # Teal accent bar at top
    canvas_obj.setFillColor(INK)
    canvas_obj.rect(0, A4[1]-18*mm, A4[0], 18*mm, fill=1, stroke=0)

    # Teal left accent line
    canvas_obj.setFillColor(TEAL)
    canvas_obj.rect(0, 0, 4, A4[1], fill=1, stroke=0)

    # Header text
    canvas_obj.setFillColor(TEAL_LIGHT)
    canvas_obj.setFont('Helvetica', 7)
    canvas_obj.drawString(15*mm, A4[1]-10*mm, 'MARQUISTEACHER ACADEMY')
    canvas_obj.setFillColor(WHITE)
    canvas_obj.drawRightString(A4[0]-15*mm, A4[1]-10*mm,
        'PERSONALISED ENGLISH LEARNING PLAN')

    # Footer
    canvas_obj.setFillColor(INK)
    canvas_obj.rect(0, 0, A4[0], 12*mm, fill=1, stroke=0)
    canvas_obj.setFillColor(GRAY)
    canvas_obj.setFont('Helvetica', 7)
    canvas_obj.drawString(15*mm, 4*mm,
        'MarquisTeacher Academy  ·  MarquisTeacher@gmail.com  ·  © 2025 Marquis Williams')
    canvas_obj.drawRightString(A4[0]-15*mm, 4*mm,
        f'Page {doc.page}')

    canvas_obj.restoreState()

# ── STYLES ────────────────────────────────────────────────────
def get_styles():
    return {
        'title': ParagraphStyle(
            'title',
            fontName='Helvetica-Bold',
            fontSize=28,
            textColor=INK,
            alignment=TA_CENTER,
            spaceAfter=4*mm,
            leading=32,
        ),
        'subtitle': ParagraphStyle(
            'subtitle',
            fontName='Helvetica',
            fontSize=13,
            textColor=GRAY,
            alignment=TA_CENTER,
            spaceAfter=2*mm,
        ),
        'level_code': ParagraphStyle(
            'level_code',
            fontName='Helvetica-Bold',
            fontSize=48,
            textColor=WHITE,
            alignment=TA_CENTER,
            leading=52,
        ),
        'level_name': ParagraphStyle(
            'level_name',
            fontName='Helvetica',
            fontSize=14,
            textColor=WHITE,
            alignment=TA_CENTER,
            spaceAfter=2*mm,
        ),
        'section_heading': ParagraphStyle(
            'section_heading',
            fontName='Helvetica-Bold',
            fontSize=14,
            textColor=INK,
            spaceBefore=4*mm,
            spaceAfter=2*mm,
            leading=18,
        ),
        'body': ParagraphStyle(
            'body',
            fontName='Helvetica',
            fontSize=10,
            textColor=INK,
            spaceAfter=2*mm,
            leading=14,
        ),
        'body_gray': ParagraphStyle(
            'body_gray',
            fontName='Helvetica',
            fontSize=9,
            textColor=GRAY,
            spaceAfter=1*mm,
            leading=13,
        ),
        'bullet': ParagraphStyle(
            'bullet',
            fontName='Helvetica',
            fontSize=9.5,
            textColor=INK,
            leftIndent=8*mm,
            spaceAfter=1.5*mm,
            leading=14,
            bulletIndent=2*mm,
        ),
        'tag': ParagraphStyle(
            'tag',
            fontName='Helvetica-Bold',
            fontSize=7,
            textColor=TEAL_DARK,
            alignment=TA_CENTER,
        ),
        'week_title': ParagraphStyle(
            'week_title',
            fontName='Helvetica-Bold',
            fontSize=9,
            textColor=WHITE,
        ),
        'week_body': ParagraphStyle(
            'week_body',
            fontName='Helvetica',
            fontSize=9,
            textColor=INK,
            leading=13,
        ),
        'right': ParagraphStyle(
            'right',
            fontName='Helvetica',
            fontSize=9,
            textColor=GRAY,
            alignment=TA_RIGHT,
        ),
    }

# ── SKILL BAR ─────────────────────────────────────────────────
def skill_bar_table(skill_name, pct, icon, styles):
    bar_width = 80 * mm
    fill_width = bar_width * (pct / 100)
    level_tag = (
        'Needs Work' if pct < 40 else
        'Developing' if pct < 65 else
        'Proficient' if pct < 85 else
        'Excellent'
    )
    tag_color = (
        colors.HexColor('#e74c3c') if pct < 40 else
        colors.HexColor('#f39c12') if pct < 65 else
        TEAL if pct < 85 else
        colors.HexColor('#27ae60')
    )

    data = [[
        Paragraph(f'{icon}  {skill_name}', styles['body']),
        Paragraph(f'{pct}%', styles['body']),
        Paragraph(level_tag, ParagraphStyle(
            'tag2', fontName='Helvetica-Bold', fontSize=7,
            textColor=tag_color, alignment=TA_RIGHT
        )),
    ]]

    t = Table(data, colWidths=[60*mm, 15*mm, 30*mm])
    t.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1*mm),
        ('TOPPADDING', (0,0), (-1,-1), 1*mm),
    ]))
    return t

# ── MAIN PDF GENERATOR ────────────────────────────────────────
def generate_learning_plan(
    student_name,
    result_code,
    self_level,
    grammar_pct,
    vocabulary_pct,
    reading_pct,
    idioms_pct,
    total_score,
    max_score,
    output_path='learning_plan.pdf'
):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=20*mm,
        rightMargin=20*mm,
        topMargin=28*mm,
        bottomMargin=22*mm,
    )

    styles  = get_styles()
    story   = []
    W       = A4[0] - 40*mm  # usable width

    level_color = LEVEL_COLORS.get(result_code, TEAL)
    level_name  = LEVEL_NAMES.get(result_code, result_code)
    next_level  = NEXT_LEVEL.get(result_code, 'C2')
    roadmap     = ROADMAPS.get(result_code, ROADMAPS['B1'])
    daily       = DAILY_PLANS.get(result_code, DAILY_PLANS['B1'])
    date_str    = datetime.now().strftime('%B %d, %Y')

    skills = {
        'Grammar':    grammar_pct,
        'Vocabulary': vocabulary_pct,
        'Reading':    reading_pct,
        'Idioms':     idioms_pct,
    }
    weak_skills   = [k for k,v in skills.items() if v < 65]
    strong_skills = [k for k,v in skills.items() if v >= 65]

    # ── PAGE 1: COVER ─────────────────────────────────────────
    story.append(Spacer(1, 8*mm))

    # Student name + date
    story.append(Paragraph(f'Prepared for {student_name}', styles['subtitle']))
    story.append(Paragraph(date_str, styles['body_gray'] if False else
        ParagraphStyle('center_gray', fontName='Helvetica', fontSize=9,
            textColor=GRAY, alignment=TA_CENTER, spaceAfter=4*mm)))
    story.append(Spacer(1, 4*mm))

    # Title
    story.append(Paragraph('Your Personalised', styles['title']))
    story.append(Paragraph('English Learning Plan', ParagraphStyle(
        'title2', fontName='Helvetica-Bold', fontSize=28,
        textColor=TEAL, alignment=TA_CENTER, spaceAfter=6*mm, leading=32
    )))
    story.append(Spacer(1, 4*mm))

    # Level badge
    badge_data = [[
        Paragraph(result_code, styles['level_code']),
    ],[
        Paragraph(level_name, styles['level_name']),
    ],[
        Paragraph('YOUR CEFR LEVEL', ParagraphStyle(
            'badge_sub', fontName='Helvetica', fontSize=7,
            textColor=colors.HexColor('#7dd8e8'), alignment=TA_CENTER,
            letterSpacing=1
        )),
    ]]
    badge = Table(badge_data, colWidths=[60*mm])
    badge.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), level_color),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4*mm),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4*mm),
        ('ROUNDEDCORNERS', [8]),
    ]))

    # Score box
    score_pct = round((total_score / max_score) * 100)
    score_data = [[
        Paragraph(f'{total_score}', ParagraphStyle(
            'score_num', fontName='Helvetica-Bold', fontSize=32,
            textColor=INK, alignment=TA_CENTER, leading=36
        )),
    ],[
        Paragraph(f'out of {max_score}', ParagraphStyle(
            'score_sub', fontName='Helvetica', fontSize=9,
            textColor=GRAY, alignment=TA_CENTER
        )),
    ],[
        Paragraph('TOTAL SCORE', ParagraphStyle(
            'score_label', fontName='Helvetica-Bold', fontSize=7,
            textColor=TEAL_DARK, alignment=TA_CENTER, letterSpacing=1
        )),
    ]]
    score_box = Table(score_data, colWidths=[50*mm])
    score_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), WHITE),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4*mm),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4*mm),
        ('BOX', (0,0), (-1,-1), 1, TEAL),
        ('ROUNDEDCORNERS', [8]),
    ]))

    # Self-assessment box
    self_name = LEVEL_NAMES.get(self_level, self_level)
    match_text = (
        'Matched!' if self_level == result_code else
        'Above self-assessment!' if LEVEL_POINTS.get(result_code,0) > LEVEL_POINTS.get(self_level,0)
        else 'Keep working toward your goal!'
    )
    self_data = [[
        Paragraph(self_level, ParagraphStyle(
            'self_num', fontName='Helvetica-Bold', fontSize=32,
            textColor=INK, alignment=TA_CENTER, leading=36
        )),
    ],[
        Paragraph(self_name, ParagraphStyle(
            'self_sub', fontName='Helvetica', fontSize=9,
            textColor=GRAY, alignment=TA_CENTER
        )),
    ],[
        Paragraph('SELF-ASSESSED', ParagraphStyle(
            'self_label', fontName='Helvetica-Bold', fontSize=7,
            textColor=GRAY, alignment=TA_CENTER, letterSpacing=1
        )),
    ]]
    self_box = Table(self_data, colWidths=[50*mm])
    self_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), PAPER),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4*mm),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4*mm),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#e5e7eb')),
        ('ROUNDEDCORNERS', [8]),
    ]))

    # Three boxes row
    boxes = Table(
        [[badge, score_box, self_box]],
        colWidths=[60*mm, 50*mm, 50*mm],
        hAlign='CENTER'
    )
    boxes.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 4*mm),
        ('RIGHTPADDING', (0,0), (-1,-1), 4*mm),
    ]))
    story.append(boxes)
    story.append(Spacer(1, 6*mm))

    # Match message
    story.append(Paragraph(f'"{match_text}"', ParagraphStyle(
        'match', fontName='Helvetica-BoldOblique', fontSize=10,
        textColor=TEAL_DARK, alignment=TA_CENTER, spaceAfter=4*mm
    )))

    story.append(HRFlowable(width=W, thickness=1, color=colors.HexColor('#e5e7eb')))
    story.append(Spacer(1, 4*mm))

    # Quick summary box
    summary_text = (
        f'{student_name}, based on your MarquisTeacher Academy assessment, '
        f'you are currently at <b>{result_code} — {level_name}</b> level. '
        f'This personalised plan is designed to guide you toward <b>{next_level} — '
        f'{LEVEL_NAMES.get(next_level, "Mastery")}</b> over the next 30 days. '
        f'Follow the daily study plan, focus on your identified weak areas, '
        f'and use your AI tutor sessions for maximum progress.'
    )
    summary = Table([[Paragraph(summary_text, styles['body'])]], colWidths=[W])
    summary.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), WHITE),
        ('BOX', (0,0), (-1,-1), 1, TEAL),
        ('LEFTPADDING', (0,0), (-1,-1), 4*mm),
        ('RIGHTPADDING', (0,0), (-1,-1), 4*mm),
        ('TOPPADDING', (0,0), (-1,-1), 3*mm),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3*mm),
        ('ROUNDEDCORNERS', [6]),
    ]))
    story.append(summary)

    # ── PAGE 2: SKILL BREAKDOWN ───────────────────────────────
    story.append(PageBreak())
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph('Skill Breakdown Analysis', styles['section_heading']))
    story.append(HRFlowable(width=W, thickness=2, color=TEAL))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph(
        'Your scores across the four core English skill areas. '
        'Areas below 65% are your priority focus zones.',
        styles['body_gray']
    ))
    story.append(Spacer(1, 4*mm))

    skill_icons = {
        'Grammar': '📐', 'Vocabulary': '📖',
        'Reading': '📰', 'Idioms': '💬'
    }

    for skill, pct in skills.items():
        color = (
            colors.HexColor('#e74c3c') if pct < 40 else
            colors.HexColor('#f39c12') if pct < 65 else
            TEAL if pct < 85 else
            colors.HexColor('#27ae60')
        )
        bar_data = [[
            Paragraph(f'{skill_icons[skill]}  {skill}', styles['body']),
            Paragraph(f'{pct}%', ParagraphStyle(
                'pct', fontName='Helvetica-Bold', fontSize=11,
                textColor=color, alignment=TA_RIGHT
            )),
        ]]
        bar_table = Table(bar_data, colWidths=[W-20*mm, 20*mm])
        bar_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 1*mm),
            ('TOPPADDING', (0,0), (-1,-1), 1*mm),
        ]))
        story.append(bar_table)

        # Progress bar
        bar_bg = Table([['']], colWidths=[W], rowHeights=[6])
        bar_bg.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#e5e7eb')),
            ('ROUNDEDCORNERS', [3]),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
            ('TOPPADDING', (0,0), (-1,-1), 0),
        ]))

        fill_w = max(W * (pct/100), 4*mm)
        bar_fill = Table([['']], colWidths=[fill_w], rowHeights=[6])
        bar_fill.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), color),
            ('ROUNDEDCORNERS', [3]),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
            ('TOPPADDING', (0,0), (-1,-1), 0),
        ]))
        story.append(bar_fill)
        story.append(Spacer(1, 4*mm))

    story.append(Spacer(1, 4*mm))

    # Strengths and weaknesses
    sw_data = [[
        Paragraph('Your Strengths', ParagraphStyle(
            'sw_h', fontName='Helvetica-Bold', fontSize=10,
            textColor=colors.HexColor('#27ae60')
        )),
        Paragraph('Priority Focus Areas', ParagraphStyle(
            'sw_h2', fontName='Helvetica-Bold', fontSize=10,
            textColor=colors.HexColor('#e74c3c')
        )),
    ],[
        Paragraph(
            ', '.join(strong_skills) if strong_skills else 'Keep working — growth is coming!',
            styles['body']
        ),
        Paragraph(
            ', '.join(weak_skills) if weak_skills else 'Excellent across all areas!',
            styles['body']
        ),
    ]]
    sw_table = Table(sw_data, colWidths=[W/2, W/2])
    sw_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#eaf7ed')),
        ('BACKGROUND', (1,0), (1,-1), colors.HexColor('#fce8e8')),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 3*mm),
        ('RIGHTPADDING', (0,0), (-1,-1), 3*mm),
        ('TOPPADDING', (0,0), (-1,-1), 3*mm),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3*mm),
        ('ROUNDEDCORNERS', [6]),
    ]))
    story.append(sw_table)

    # ── PAGE 3: STRATEGIES ────────────────────────────────────
    story.append(PageBreak())
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph('Your Personalised Learning Strategies', styles['section_heading']))
    story.append(HRFlowable(width=W, thickness=2, color=TEAL))
    story.append(Spacer(1, 3*mm))

    for skill, pct in skills.items():
        strategy = SKILL_STRATEGIES[skill]
        is_weak  = pct < 65
        tips     = strategy['weak'] if is_weak else strategy['strong']
        bg_color = colors.HexColor('#fef9ec') if is_weak else colors.HexColor('#f0fdf4')
        border   = colors.HexColor('#f39c12') if is_weak else colors.HexColor('#27ae60')

        header_data = [[
            Paragraph(
                f'{strategy["icon"]}  {skill}  —  {pct}%',
                ParagraphStyle('skill_h', fontName='Helvetica-Bold',
                    fontSize=11, textColor=INK)
            ),
            Paragraph(
                'PRIORITY' if is_weak else 'STRENGTH',
                ParagraphStyle('skill_tag', fontName='Helvetica-Bold',
                    fontSize=7, textColor=border, alignment=TA_RIGHT,
                    letterSpacing=1)
            ),
        ]]
        header = Table(header_data, colWidths=[W-20*mm, 20*mm])
        header.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('BACKGROUND', (0,0), (-1,-1), bg_color),
            ('LEFTPADDING', (0,0), (-1,-1), 3*mm),
            ('RIGHTPADDING', (0,0), (-1,-1), 3*mm),
            ('TOPPADDING', (0,0), (-1,-1), 2*mm),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2*mm),
        ]))
        story.append(header)

        tip_rows = [[Paragraph(
            f'{strategy["description"]}', styles['body_gray']
        )]]
        for tip in tips:
            tip_rows.append([Paragraph(f'→  {tip}', styles['bullet'])])

        tips_table = Table(tip_rows, colWidths=[W])
        tips_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), bg_color),
            ('LEFTPADDING', (0,0), (-1,-1), 3*mm),
            ('RIGHTPADDING', (0,0), (-1,-1), 3*mm),
            ('TOPPADDING', (0,0), (-1,-1), 1*mm),
            ('BOTTOMPADDING', (0,0), (-1,-1), 1*mm),
            ('BOX', (0,0), (-1,-1), 1.5, border),
            ('ROUNDEDCORNERS', [6]),
        ]))
        story.append(tips_table)
        story.append(Spacer(1, 4*mm))

    # ── PAGE 4: 30-DAY ROADMAP ────────────────────────────────
    story.append(PageBreak())
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph('Your 30-Day Learning Roadmap', styles['section_heading']))
    story.append(HRFlowable(width=W, thickness=2, color=TEAL))
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph(
        f'Goal: {roadmap["goal"]}', ParagraphStyle(
            'goal', fontName='Helvetica-BoldOblique', fontSize=10,
            textColor=TEAL_DARK, spaceAfter=4*mm
        )
    ))

    week_data = []
    for week_title, week_content in roadmap['weeks']:
        week_data.append([
            Paragraph(week_title, styles['week_title']),
            Paragraph(week_content, styles['week_body']),
        ])

    week_table = Table(week_data, colWidths=[25*mm, W-25*mm])
    week_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), INK),
        ('BACKGROUND', (1,0), (1,-1), WHITE),
        ('BACKGROUND', (1,1), (1,1), PAPER),
        ('BACKGROUND', (1,3), (1,3), PAPER),
        ('TEXTCOLOR', (0,0), (0,-1), WHITE),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 3*mm),
        ('RIGHTPADDING', (0,0), (-1,-1), 3*mm),
        ('TOPPADDING', (0,0), (-1,-1), 4*mm),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4*mm),
        ('LINEBELOW', (0,0), (-1,-2), 1, colors.HexColor('#e5e7eb')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#e5e7eb')),
    ]))
    story.append(week_table)
    story.append(Spacer(1, 6*mm))

    # Daily study plan
    story.append(Paragraph('Daily Study Plan', styles['section_heading']))
    story.append(HRFlowable(width=W, thickness=1, color=colors.HexColor('#e5e7eb')))
    story.append(Spacer(1, 2*mm))

    daily_data = [[
        Paragraph('Time Slot', ParagraphStyle(
            'dh', fontName='Helvetica-Bold', fontSize=8,
            textColor=WHITE
        )),
        Paragraph('Activity', ParagraphStyle(
            'dh2', fontName='Helvetica-Bold', fontSize=8,
            textColor=WHITE
        )),
    ]]
    for slot, activity in daily:
        daily_data.append([
            Paragraph(slot, styles['body_gray']),
            Paragraph(activity, styles['body']),
        ])

    daily_table = Table(daily_data, colWidths=[40*mm, W-40*mm])
    daily_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), INK),
        ('BACKGROUND', (0,1), (-1,-1), WHITE),
        ('ROWBACKGROUNDS', (0,1), (-1,-1),
            [WHITE, colors.HexColor('#f8fafc')]),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 3*mm),
        ('RIGHTPADDING', (0,0), (-1,-1), 3*mm),
        ('TOPPADDING', (0,0), (-1,-1), 3*mm),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3*mm),
        ('LINEBELOW', (0,0), (-1,-2), 0.5, colors.HexColor('#e5e7eb')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#e5e7eb')),
    ]))
    story.append(daily_table)

    # ── PAGE 5: NEXT STEPS ────────────────────────────────────
    story.append(PageBreak())
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph('Your Next Steps', styles['section_heading']))
    story.append(HRFlowable(width=W, thickness=2, color=TEAL))
    story.append(Spacer(1, 4*mm))

    steps = [
        ('01', 'Start Today',
         'Begin with Day 1 of your study plan. Even 15 minutes of focused practice today sets the momentum for everything that follows.'),
        ('02', 'Use Your AI Tutor',
         'Sign up for your MarquisTeacher AI Tutor sessions. Your tutor knows your results and will focus exactly on your weak areas from day one.'),
        ('03', 'Track Your Progress',
         'After 30 days, retake the MarquisTeacher English Assessment. Compare your new skill breakdown with this plan to measure real growth.'),
        ('04', 'Book a Free Consultation',
         'Connect with Marquis Williams directly for personalised guidance, goal setting, and a conversation about your English learning journey.'),
    ]

    for num, title, desc in steps:
        step_data = [[
            Paragraph(num, ParagraphStyle(
                'step_num', fontName='Helvetica-Bold', fontSize=22,
                textColor=TEAL, alignment=TA_CENTER, leading=26
            )),
            [
                Paragraph(title, ParagraphStyle(
                    'step_title', fontName='Helvetica-Bold', fontSize=11,
                    textColor=INK, spaceAfter=1*mm
                )),
                Paragraph(desc, styles['body_gray']),
            ]
        ]]
        step_table = Table(step_data, colWidths=[18*mm, W-18*mm])
        step_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('BACKGROUND', (0,0), (-1,-1), WHITE),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#e5e7eb')),
            ('LEFTPADDING', (0,0), (-1,-1), 3*mm),
            ('RIGHTPADDING', (0,0), (-1,-1), 3*mm),
            ('TOPPADDING', (0,0), (-1,-1), 3*mm),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3*mm),
            ('LINEAFTER', (0,0), (0,-1), 2, TEAL),
            ('ROUNDEDCORNERS', [6]),
        ]))
        story.append(step_table)
        story.append(Spacer(1, 3*mm))

    story.append(Spacer(1, 6*mm))

    # Contact CTA
    cta_data = [[
        Paragraph(
            'Ready to accelerate your English?\n'
            'Email us: MarquisTeacher@gmail.com',
            ParagraphStyle(
                'cta', fontName='Helvetica-Bold', fontSize=12,
                textColor=WHITE, alignment=TA_CENTER, leading=18
            )
        )
    ]]
    cta = Table(cta_data, colWidths=[W])
    cta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), INK),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 6*mm),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6*mm),
        ('ROUNDEDCORNERS', [8]),
    ]))
    story.append(cta)

    story.append(Spacer(1, 4*mm))
    story.append(Paragraph(
        f'© 2025 Marquis Williams & MarquisTeacher Academy  ·  '
        f'Plan generated {date_str}  ·  '
        f'Valid for 30 days from issue date',
        ParagraphStyle('footer_note', fontName='Helvetica', fontSize=7,
            textColor=GRAY, alignment=TA_CENTER)
    ))

    # ── BUILD ─────────────────────────────────────────────────
    doc.build(story, onFirstPage=add_page_background,
              onLaterPages=add_page_background)

    print(f'PDF generated: {output_path}')
    return output_path


# ── ENTRY POINT ───────────────────────────────────────────────
if __name__ == '__main__':
    import sys

    # Called from Node.js with command line arguments
    if len(sys.argv) > 1:
        generate_learning_plan(
            student_name   = sys.argv[1],
            result_code    = sys.argv[2],
            self_level     = sys.argv[3],
            grammar_pct    = int(sys.argv[4]),
            vocabulary_pct = int(sys.argv[5]),
            reading_pct    = int(sys.argv[6]),
            idioms_pct     = int(sys.argv[7]),
            total_score    = int(sys.argv[8]),
            max_score      = int(sys.argv[9]),
            output_path    = sys.argv[10]
        )
    else:
        # Test run
        generate_learning_plan(
            student_name   = 'Marquis Williams',
            result_code    = 'B2',
            self_level     = 'B1',
            grammar_pct    = 72,
            vocabulary_pct = 45,
            reading_pct    = 88,
            idioms_pct     = 60,
            total_score    = 48,
            max_score      = 72,
            output_path    = '/tmp/test_learning_plan.pdf'
        )
