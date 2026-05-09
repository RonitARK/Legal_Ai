import io
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

# ── Brand colours ──────────────────────────────────────────────────────────
NAVY      = colors.HexColor("#1B2B4B")
GOLD      = colors.HexColor("#C9A84C")
RED_ALERT = colors.HexColor("#D94F3D")
AMBER     = colors.HexColor("#E8953A")
GREEN_OK  = colors.HexColor("#2E7D52")
LIGHT_BG  = colors.HexColor("#F5F7FA")
MID_GREY  = colors.HexColor("#6B7280")
BORDER    = colors.HexColor("#D1D5DB")

W, H = A4  # 595.27 x 841.89 points


# ── Helper: score colour ───────────────────────────────────────────────────
def _score_colour(score: int) -> colors.Color:
    if score >= 75:
        return GREEN_OK
    if score >= 50:
        return AMBER
    return RED_ALERT


def _score_label(score: int) -> str:
    if score >= 75:
        return "MODERATE RISK"
    if score >= 50:
        return "HIGH RISK"
    return "CRITICAL RISK"


# ── Main function ──────────────────────────────────────────────────────────
def generate_audit_report(audit_result: dict, company_name: str = "Your Company") -> bytes:
    """
    audit_result must contain:
        score       : int  (0–100)
        gaps        : list of {
                        section  : str   e.g. "Section 14(1), Code on Wages"
                        issue    : str   short description
                        severity : str   "Critical" | "High" | "Medium"
                        fix      : str   suggested replacement language
                      }
        summary     : str  (optional — 1-2 line AI summary)

    Returns raw PDF bytes.
    """
    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=16 * mm,
        bottomMargin=16 * mm,
    )

    styles = getSampleStyleSheet()

    # ── Custom styles ──────────────────────────────────────────────────────
    def S(name, **kw):
        return ParagraphStyle(name, **kw)

    sty_brand  = S("brand",  fontName="Helvetica-Bold", fontSize=20, textColor=NAVY,  spaceAfter=2)
    sty_tag    = S("tag",    fontName="Helvetica",      fontSize=9,  textColor=GOLD,  spaceAfter=0)
    sty_h1     = S("h1",     fontName="Helvetica-Bold", fontSize=15, textColor=NAVY,  spaceBefore=10, spaceAfter=4)
    sty_h2     = S("h2",     fontName="Helvetica-Bold", fontSize=11, textColor=NAVY,  spaceBefore=8,  spaceAfter=3)
    sty_body   = S("body",   fontName="Helvetica",      fontSize=9,  textColor=colors.HexColor("#374151"), leading=14, spaceAfter=4)
    sty_small  = S("small",  fontName="Helvetica",      fontSize=8,  textColor=MID_GREY, leading=12)
    sty_fix    = S("fix",    fontName="Helvetica-Oblique", fontSize=8.5, textColor=colors.HexColor("#1D4ED8"), leading=13, leftIndent=6)
    sty_section= S("section",fontName="Helvetica-Bold", fontSize=8,  textColor=NAVY)
    sty_footer = S("footer", fontName="Helvetica",      fontSize=7.5,textColor=MID_GREY, alignment=TA_CENTER)

    score  = int(audit_result.get("overall_score", audit_result.get("score", 0)))
    gaps   = audit_result.get("gaps", [])
    summary = audit_result.get("summary", "")
    now    = datetime.now().strftime("%d %B %Y, %I:%M %p")
    sc     = _score_colour(score)
    label  = _score_label(score)

    story = []

    # ── HEADER ─────────────────────────────────────────────────────────────
    header_data = [[
        Paragraph("LegalAI India", sty_brand),
        Paragraph(f"<b>{company_name}</b><br/><font color='#6B7280' size='8'>"
                  f"HR Policy Compliance Report &nbsp;·&nbsp; {now}</font>",
                  ParagraphStyle("rh", fontName="Helvetica", fontSize=9,
                                 textColor=NAVY, alignment=TA_RIGHT, leading=14))
    ]]
    header_tbl = Table(header_data, colWidths=[W * 0.5 - 18 * mm, W * 0.5 - 18 * mm])
    header_tbl.setStyle(TableStyle([
        ("VALIGN",  (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING",    (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    story.append(header_tbl)
    story.append(Paragraph("AI-powered compliance audit against all four Indian Labour Codes", sty_tag))
    story.append(HRFlowable(width="100%", thickness=2, color=GOLD, spaceAfter=10))

    # ── SCORE BANNER ───────────────────────────────────────────────────────
    sc          = _score_colour(score)
    label       = _score_label(score)
    sc_hex      = sc.hexval()
    sc_hex_clean = "#" + sc_hex.replace("0x", "").replace("x", "")
    score_data = [[
        Paragraph(f"<font size='36' color='#{sc_hex_clean}'><b>{score}</b></font>"
                  f"<font size='14' color='#6B7280'>/100</font>",
                  ParagraphStyle("sc", fontName="Helvetica-Bold", fontSize=36,
                                 alignment=TA_CENTER, leading=42)),
        [
            Paragraph("COMPLIANCE SCORE", S("cslbl", fontName="Helvetica-Bold",
                                             fontSize=8, textColor=MID_GREY, spaceAfter=3)),
            Paragraph(label, S("cslabel2", fontName="Helvetica-Bold", fontSize=14,
                                textColor=sc, spaceAfter=4)),
            Paragraph(
                f"<b>{len(gaps)}</b> compliance gap{'s' if len(gaps) != 1 else ''} found across "
                f"the Code on Wages, Industrial Relations Code, "
                f"Social Security Code &amp; OSH Code.",
                S("csub", fontName="Helvetica", fontSize=9,
                  textColor=colors.HexColor("#374151"), leading=13)
            ),
        ]
    ]]
    score_tbl = Table(score_data, colWidths=[55 * mm, W - 55 * mm - 36 * mm])
    score_tbl.setStyle(TableStyle([
        ("VALIGN",          (0, 0), (-1, -1), "MIDDLE"),
        ("BACKGROUND",      (0, 0), (-1, -1), LIGHT_BG),
        ("ROUNDEDCORNERS",  [4, 4, 4, 4]),
        ("BOX",             (0, 0), (-1, -1), 0.5, BORDER),
        ("LEFTPADDING",     (0, 0), (-1, -1), 12),
        ("RIGHTPADDING",    (0, 0), (-1, -1), 12),
        ("TOPPADDING",      (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING",   (0, 0), (-1, -1), 10),
    ]))
    story.append(score_tbl)
    story.append(Spacer(1, 8))

    # ── SUMMARY ────────────────────────────────────────────────────────────
    if summary:
        story.append(Paragraph("Executive Summary", sty_h2))
        story.append(Paragraph(summary, sty_body))
        story.append(Spacer(1, 4))

    # ── GAPS TABLE ─────────────────────────────────────────────────────────
    story.append(Paragraph("Compliance Gaps — Detailed Findings", sty_h1))
    story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER, spaceAfter=6))

    SEV_COLOUR = {
        "critical": RED_ALERT,
        "high":     AMBER,
        "medium":   colors.HexColor("#D97706"),
        "low":      GREEN_OK,
    }

    for i, gap in enumerate(gaps, 1):
        severity = gap.get("severity", "High")
        sev_col  = SEV_COLOUR.get(severity.lower(), AMBER)
        section  = gap.get("section", "—")
        issue    = gap.get("issue", "")
        fix      = gap.get("fix", "")

        # severity badge
        badge = Table(
            [[Paragraph(severity.upper(),
                        S("badge", fontName="Helvetica-Bold", fontSize=7,
                          textColor=colors.white, alignment=TA_CENTER))]],
            colWidths=[18 * mm]
        )
        badge.setStyle(TableStyle([
            ("BACKGROUND",    (0, 0), (-1, -1), sev_col),
            ("TOPPADDING",    (0, 0), (-1, -1), 2),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ("LEFTPADDING",   (0, 0), (-1, -1), 3),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 3),
        ]))

        gap_inner = [
            [
                Paragraph(f"<b>#{i} &nbsp; {section}</b>",
                          S("gi", fontName="Helvetica-Bold", fontSize=9, textColor=NAVY)),
                badge,
            ],
            [
                Paragraph(issue, sty_body),
                "",
            ],
        ]
        if fix:
            gap_inner.append([
                Paragraph(f"<b>Suggested fix:</b> {fix}", sty_fix),
                "",
            ])

        gap_tbl = Table(
            gap_inner,
            colWidths=[W - 36 * mm - 26 * mm, 26 * mm],
        )
        gap_tbl.setStyle(TableStyle([
            ("VALIGN",        (0, 0), (-1, -1), "TOP"),
            ("ALIGN",         (1, 0), (1, 0),  "RIGHT"),
            ("SPAN",          (0, 1), (1, 1)),
            ("SPAN",          (0, 2), (1, 2)),
            ("BACKGROUND",    (0, 0), (-1, -1), colors.white),
            ("BOX",           (0, 0), (-1, -1), 0.5, BORDER),
            ("LINEBELOW",     (0, 0), (-1, 0),  0.5, LIGHT_BG),
            ("TOPPADDING",    (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ("LEFTPADDING",   (0, 0), (-1, -1), 10),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
        ]))

        story.append(KeepTogether([gap_tbl, Spacer(1, 5)]))

    # ── CODES REFERENCE ────────────────────────────────────────────────────
    story.append(Spacer(1, 6))
    story.append(Paragraph("Codes Covered in This Audit", sty_h2))
    codes = [
        ["Code on Wages, 2019",                  "136 checkpoints — wages, overtime, payment timelines"],
        ["Industrial Relations Code, 2020",       "Dispute resolution, standing orders, layoff rules"],
        ["Code on Social Security, 2020",         "PF, ESIC, gratuity, maternity, gig worker benefits"],
        ["OSH Code, 2020",                        "Safety, working hours, contractor obligations"],
    ]
    codes_hdr = [["Labour Code", "Key Compliance Areas"]]
    codes_tbl = Table(
        codes_hdr + codes,
        colWidths=[70 * mm, W - 70 * mm - 36 * mm],
    )
    codes_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0),  NAVY),
        ("TEXTCOLOR",     (0, 0), (-1, 0),  colors.white),
        ("FONTNAME",      (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, -1), 8),
        ("FONTNAME",      (0, 1), (-1, -1), "Helvetica"),
        ("TEXTCOLOR",     (0, 1), (-1, -1), colors.HexColor("#374151")),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [colors.white, LIGHT_BG]),
        ("GRID",          (0, 0), (-1, -1), 0.4, BORDER),
        ("TOPPADDING",    (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING",   (0, 0), (-1, -1), 8),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
    ]))
    story.append(codes_tbl)

    # ── DISCLAIMER ─────────────────────────────────────────────────────────
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER, spaceAfter=5))
    story.append(Paragraph(
        "This report is generated by LegalAI India's AI compliance engine and is intended for "
        "informational purposes only. It does not constitute legal advice. For matters involving "
        "litigation, prosecution, or complex state-specific compliance, consult a qualified "
        "labour law advocate. &nbsp;·&nbsp; <b>legalai.in</b>",
        sty_footer
    ))

    doc.build(story)
    buffer.seek(0)
    return buffer.read()