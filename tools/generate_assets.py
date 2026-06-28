from pathlib import Path
from textwrap import wrap

from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


SITE = Path(__file__).resolve().parents[1]
ASSETS = SITE / "assets"
ASSETS.mkdir(exist_ok=True)

INK = HexColor("#101418")
PAPER = HexColor("#f5f1ea")
EMBER = HexColor("#d66b35")
AMBER = HexColor("#f0b35a")
MUTED = HexColor("#665f56")
LINE = HexColor("#e2d8ca")


def draw_wrapped(c, text, x, y, width_chars=86, size=10.5, leading=14, color=MUTED, font="Helvetica"):
    c.setFillColor(color)
    c.setFont(font, size)
    for paragraph in text.split("\n"):
        lines = wrap(paragraph, width_chars) or [""]
        for line in lines:
            c.drawString(x, y, line)
            y -= leading
        y -= leading * 0.35
    return y


def draw_pdf(path, route, subtitle, bullets, note):
    c = canvas.Canvas(str(path), pagesize=A4)
    w, h = A4
    margin = 48

    c.setFillColor(PAPER)
    c.rect(0, 0, w, h, stroke=0, fill=1)
    c.setStrokeColor(LINE)
    for offset in range(0, int(w), 36):
        c.line(offset, 0, offset, h)
    for offset in range(0, int(h), 36):
        c.line(0, offset, w, offset)

    c.setFillColor(INK)
    c.roundRect(margin, h - 185, w - margin * 2, 128, 8, stroke=0, fill=1)
    c.setFillColor(AMBER)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(margin + 24, h - 92, "ARCHEGON PROJECT BRIEF")
    c.setFillColor(HexColor("#fffaf1"))
    c.setFont("Helvetica-Bold", 30)
    c.drawString(margin + 24, h - 132, route)
    c.setFont("Helvetica", 12)
    c.drawString(margin + 24, h - 156, subtitle)

    y = h - 230
    c.setFillColor(EMBER)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(margin, y, "Working thesis")
    y -= 24
    y = draw_wrapped(
        c,
        "Archegon develops geothermal-powered data centres - pairing 24/7 firm clean power "
        "with AI inference, where the grid cannot reach and intermittent renewables cannot follow.",
        margin,
        y,
        width_chars=84,
        size=11,
        leading=15,
        color=INK,
    )

    y -= 10
    c.setFillColor(EMBER)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(margin, y, "Route summary")
    y -= 24
    for bullet in bullets:
        c.setFillColor(EMBER)
        c.circle(margin + 4, y + 4, 2.5, stroke=0, fill=1)
        y = draw_wrapped(c, bullet, margin + 18, y, width_chars=78, size=10.5, leading=14, color=INK)
        y -= 3

    y -= 12
    c.setFillColor(EMBER)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(margin, y, "Diligence note")
    y -= 24
    draw_wrapped(c, note, margin, y, width_chars=84, size=10.5, leading=14, color=MUTED)

    c.setStrokeColor(EMBER)
    c.setLineWidth(3)
    c.line(margin, 110, margin, 66)
    disclaimer = (
        "Nothing in this document or on archegon.com constitutes an offer or invitation to invest, "
        "financial advice, or a financial promotion. All figures are illustrative, built from public "
        "benchmarks where stated, and subject to verification and due diligence."
    )
    draw_wrapped(c, disclaimer, margin + 14, 103, width_chars=90, size=8.7, leading=11, color=MUTED)

    c.setFillColor(MUTED)
    c.setFont("Helvetica", 8)
    c.drawString(margin, 34, "archegon.com | hello@archegon.com | Preliminary project brief")
    c.showPage()
    c.save()


def load_font(size, bold=False):
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            continue
    return ImageFont.load_default()


def draw_og_card():
    img = Image.new("RGB", (1200, 630), "#101418")
    draw = ImageDraw.Draw(img)
    for radius, color in [(520, "#3a211d"), (430, "#5d2f24"), (340, "#8f4f34"), (250, "#d66b35"), (160, "#f0b35a")]:
        draw.ellipse((780 - radius, 445 - radius, 780 + radius, 445 + radius), outline=color, width=3)
    for x in range(0, 1200, 48):
        draw.line((x, 0, x, 630), fill="#1a2428", width=1)
    for y in range(0, 630, 48):
        draw.line((0, y, 1200, y), fill="#1a2428", width=1)

    draw.text((72, 74), "ARCHEGON", fill="#f0b35a", font=load_font(34, True))
    draw.text((72, 166), "Bringing compute\nto the heat.", fill="#fffaf1", font=load_font(74, True), spacing=8)
    draw.text(
        (76, 400),
        "Geothermal-powered data centres - firm clean power for AI inference.",
        fill="#d9d1c5",
        font=load_font(28),
    )
    draw.line((76, 512, 420, 512), fill="#d66b35", width=6)
    draw.text(
        (76, 536),
        "Investor and partner interest only - not an investment offer.",
        fill="#d9d1c5",
        font=load_font(20),
    )
    img.save(ASSETS / "og-card.png", quality=92)


def main():
    draw_pdf(
        ASSETS / "archegon-new-zealand-project-brief.pdf",
        "New Zealand - The Build",
        "Grid-adjacent geothermal AI campus",
        [
            "Proven, operating geothermal context with a lower-risk infrastructure development path.",
            "Temperate climate, natural cooling potential, water availability, and fast-track consenting.",
            "A preliminary 100 MW+ AI campus concept to be validated with partners and site diligence.",
            "Best suited to infrastructure, energy, and strategic compute partners seeking a buildable route this decade.",
        ],
        "This is a preliminary branded summary created from the current Archegon thesis. "
        "Replace it with the founder-approved full business plan before broad investor or partner circulation.",
    )

    draw_pdf(
        ASSETS / "archegon-australia-project-brief.pdf",
        "Australia - The Bet",
        "Off-grid Cooper Basin compute hub",
        [
            "World-class hot-dry-rock thesis with behind-the-meter, fully off-grid potential.",
            "Higher technical and development risk, with multi-GW scale headroom if validated.",
            "Power-stack ownership and optional lithium co-production are research-stage upside themes.",
            "Best suited to geothermal, infrastructure, energy, and frontier compute partners willing to diligence the resource.",
        ],
        "This is a preliminary branded summary created from the current Archegon thesis. "
        "Replace it with the founder-approved full business plan before broad investor or partner circulation.",
    )

    draw_og_card()


if __name__ == "__main__":
    main()
