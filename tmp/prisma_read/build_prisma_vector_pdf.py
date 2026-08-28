from pathlib import Path

from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import landscape
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT = Path("/Users/annalenz/Desktop/ChronicNoise_Rodents/Prenatal_Chronic_Noise")
OUTPUT = ROOT / "output/pdf/PCN_PRISMA_flowchart_vector.pdf"

PX_WIDTH = 4500
PX_HEIGHT = 3300
PAGE_WIDTH = 15 * inch
PAGE_HEIGHT = 11 * inch
SCALE = PAGE_WIDTH / PX_WIDTH

ARIAL = "/System/Library/Fonts/Supplemental/Arial.ttf"
ARIAL_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
pdfmetrics.registerFont(TTFont("Arial", ARIAL))
pdfmetrics.registerFont(TTFont("Arial-Bold", ARIAL_BOLD))

NAVY = HexColor("#17365D")
TEAL = HexColor("#13698B")
LIGHT_BLUE = HexColor("#D9E8F6")
PALE_BLUE = HexColor("#EEF3F7")
PEACH = HexColor("#F7D1B0")
PALE_PEACH = HexColor("#FBE2D3")
RAIL_TEXT = HexColor("#9B4A18")


def x(value):
    return value * SCALE


def y(value):
    return PAGE_HEIGHT - value * SCALE


def rect_to_pdf(box):
    x1, y1, x2, y2 = box
    return x(x1), y(y2), x(x2 - x1), x(y2 - y1)


def rounded_box(pdf, box, fill, outline=TEAL, stroke_width=7, radius=18):
    px, py, width, height = rect_to_pdf(box)
    pdf.setFillColor(fill)
    pdf.setStrokeColor(outline)
    pdf.setLineWidth(x(stroke_width))
    pdf.roundRect(px, py, width, height, x(radius), stroke=1, fill=1)


def wrapped_lines(text, font_name, font_size, max_width):
    result = []
    for paragraph in text.split("\n"):
        words = paragraph.split()
        if not words:
            result.append("")
            continue
        line = words[0]
        for word in words[1:]:
            trial = f"{line} {word}"
            if pdfmetrics.stringWidth(trial, font_name, font_size) <= max_width:
                line = trial
            else:
                result.append(line)
                line = word
        result.append(line)
    return result


def centered_text(pdf, box, text, font_name, font_px, color=NAVY, leading_px=None, pad_px=34):
    x1, y1, x2, y2 = box
    font_size = x(font_px)
    leading = x(leading_px if leading_px is not None else font_px * 1.12)
    lines = wrapped_lines(text, font_name, font_size, x((x2 - x1) - 2 * pad_px))
    block_height = leading * len(lines)
    centre_x = x((x1 + x2) / 2)
    top_y = y((y1 + y2) / 2) + block_height / 2 - leading * 0.79
    pdf.setFillColor(color)
    pdf.setFont(font_name, font_size)
    for index, line in enumerate(lines):
        pdf.drawCentredString(centre_x, top_y - index * leading, line)


def left_text(pdf, px, py, text, font_name, font_px, color=NAVY):
    pdf.setFillColor(color)
    pdf.setFont(font_name, x(font_px))
    pdf.drawString(x(px), y(py), text)


def line(pdf, points, color=TEAL, stroke_width=6):
    pdf.setStrokeColor(color)
    pdf.setLineWidth(x(stroke_width))
    path = pdf.beginPath()
    path.moveTo(x(points[0][0]), y(points[0][1]))
    for px, py in points[1:]:
        path.lineTo(x(px), y(py))
    pdf.drawPath(path, stroke=1, fill=0)


def arrow(pdf, points, color=TEAL, stroke_width=8, head=25):
    line(pdf, points, color=color, stroke_width=stroke_width)
    x1, y1 = points[-2]
    x2, y2 = points[-1]
    if abs(x2 - x1) >= abs(y2 - y1):
        if x2 > x1:
            polygon = [(x2, y2), (x2 - head, y2 - head * 0.65), (x2 - head, y2 + head * 0.65)]
        else:
            polygon = [(x2, y2), (x2 + head, y2 - head * 0.65), (x2 + head, y2 + head * 0.65)]
    elif y2 > y1:
        polygon = [(x2, y2), (x2 - head * 0.65, y2 - head), (x2 + head * 0.65, y2 - head)]
    else:
        polygon = [(x2, y2), (x2 - head * 0.65, y2 + head), (x2 + head * 0.65, y2 + head)]
    path = pdf.beginPath()
    path.moveTo(x(polygon[0][0]), y(polygon[0][1]))
    path.lineTo(x(polygon[1][0]), y(polygon[1][1]))
    path.lineTo(x(polygon[2][0]), y(polygon[2][1]))
    path.close()
    pdf.setFillColor(color)
    pdf.drawPath(path, stroke=0, fill=1)


def create_pdf(path):
    path.parent.mkdir(parents=True, exist_ok=True)
    pdf = canvas.Canvas(str(path), pagesize=(PAGE_WIDTH, PAGE_HEIGHT), pageCompression=1)
    pdf.setTitle("PRISMA flowchart - prenatal chronic noise meta-analysis")
    pdf.setAuthor("Anna Lenz")
    pdf.setSubject("Editable vector PRISMA flowchart")

    pdf.setFillColor(white)
    pdf.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, stroke=0, fill=1)

    rounded_box(pdf, (270, 65, 4380, 175), LIGHT_BLUE, LIGHT_BLUE, 1, 38)
    centered_text(pdf, (270, 65, 4380, 175), "Records identified from databases and search sources", "Arial-Bold", 52, TEAL)

    rails = [
        ((45, 210, 190, 1100), "Identification"),
        ((45, 1140, 190, 2390), "Screening"),
        ((45, 2430, 190, 3210), "Included"),
    ]
    for box, label in rails:
        rounded_box(pdf, box, PEACH, PEACH, 1, 65)
        x1, y1, x2, y2 = box
        pdf.saveState()
        pdf.translate(x((x1 + x2) / 2), y((y1 + y2) / 2))
        pdf.rotate(90)
        pdf.setFillColor(RAIL_TEXT)
        pdf.setFont("Arial-Bold", x(39))
        pdf.drawCentredString(0, -x(13), label)
        pdf.restoreState()

    top_source_boxes = [
        ((280, 230, 1220, 435), "Scopus\n(n = 1,404)"),
        ((1290, 230, 2230, 435), "Web of Science\n(n = 1,842)"),
        ((2300, 230, 3240, 435), "PubMed\n(n = 1,056)"),
        ((3310, 230, 4250, 435), "PsycINFO\n(n = 408)"),
    ]
    lower_source_boxes = [
        ((350, 520, 1450, 725), "OpenAlex\n(n = 681)"),
        ((1700, 520, 2800, 725), "Google Scholar\nsupplementary search\n(n = 489)"),
        ((3050, 520, 4150, 725), "BASE\n(n = 9)"),
    ]
    for box, text in top_source_boxes + lower_source_boxes:
        rounded_box(pdf, box, white, TEAL, 7, 4)
        centered_text(pdf, box, text, "Arial-Bold", 40, NAVY, 45)

    upper_trunk_y = 475
    upper_centres = []
    for box, _ in top_source_boxes:
        centre = (box[0] + box[2]) / 2
        upper_centres.append(centre)
        line(pdf, [(centre, box[3]), (centre, upper_trunk_y)])
    line(pdf, [(min(upper_centres), upper_trunk_y), (max(upper_centres), upper_trunk_y)])

    merge_x = 1550
    lower_trunk_y = 790
    line(pdf, [(merge_x, upper_trunk_y), (merge_x, lower_trunk_y)])
    lower_centres = []
    for box, _ in lower_source_boxes:
        centre = (box[0] + box[2]) / 2
        lower_centres.append(centre)
        line(pdf, [(centre, box[3]), (centre, lower_trunk_y)])
    line(pdf, [(min(lower_centres), lower_trunk_y), (max(lower_centres), lower_trunk_y)])

    records = (620, 870, 2080, 1050)
    duplicates = (2460, 850, 4260, 1090)
    rounded_box(pdf, records, white)
    centered_text(pdf, records, "Records identified\n(n = 5,889)", "Arial-Bold", 48)
    arrow(pdf, [(merge_x, lower_trunk_y), (merge_x, 825), (1350, 825), (1350, records[1])])
    rounded_box(pdf, duplicates, PALE_BLUE)
    left_text(pdf, 2510, 930, "Duplicates removed before screening (n = 3,576)", "Arial-Bold", 38)
    left_text(pdf, 2510, 995, "Includes duplicate BASE records", "Arial", 38)
    arrow(pdf, [(records[2], 960), (duplicates[0], 960)])

    unique = (620, 1200, 2080, 1380)
    rounded_box(pdf, unique, white)
    centered_text(pdf, unique, "Unique records screened\n(n = 2,313)", "Arial-Bold", 48)
    arrow(pdf, [(1350, records[3]), (1350, unique[1])])

    abstract_included = (620, 1540, 2080, 1735)
    rounded_box(pdf, abstract_included, white)
    centered_text(pdf, abstract_included, "Included at title-and-\nabstract stage\n(n = 87)", "Arial-Bold", 48, leading_px=50)
    arrow(pdf, [(1350, unique[3]), (1350, abstract_included[1])])

    abstract_excluded = (2460, 1515, 4260, 1760)
    rounded_box(pdf, abstract_excluded, PALE_BLUE)
    centered_text(pdf, abstract_excluded, "Records excluded after title-and-abstract screening\n(n = 2,226)", "Arial", 38, leading_px=43)
    arrow(pdf, [(abstract_included[2], 1638), (abstract_excluded[0], 1638)])

    full_text_included = (620, 2070, 2080, 2260)
    rounded_box(pdf, full_text_included, white)
    centered_text(pdf, full_text_included, "Included at full-text stage\n(n = 12)", "Arial-Bold", 48, leading_px=52)
    arrow(pdf, [(1350, abstract_included[3]), (1350, full_text_included[1])])

    full_text_excluded = (2460, 1940, 4260, 2390)
    rounded_box(pdf, full_text_excluded, PALE_BLUE)
    left_text(pdf, 2510, 2018, "Full-text reports excluded, with reasons (n = 75)", "Arial-Bold", 38)
    reason_lines = [
        "Wrong exposure (n = 60)",
        "Wrong outcome (n = 4)",
        "Wrong publication type (n = 4)",
        "Wrong population (n = 4)",
        "Foreign language (n = 2)",
        "Full text not available (n = 1)",
    ]
    for index, reason in enumerate(reason_lines):
        left_text(pdf, 2510, 2088 + index * 52, reason, "Arial", 34)
    arrow(pdf, [(full_text_included[2], 2165), (full_text_excluded[0], 2165)])

    additional = (2460, 2500, 4260, 2710)
    rounded_box(pdf, additional, PALE_PEACH)
    centered_text(pdf, additional, "Other sources (benchmark set)\n(n = 4)", "Arial-Bold", 48, leading_px=52)

    final = (1150, 2920, 2750, 3150)
    rounded_box(pdf, final, PEACH)
    centered_text(pdf, final, "Studies included in\nthe meta-analysis\n(n = 16)", "Arial-Bold", 48, leading_px=50)
    arrow(pdf, [(1350, full_text_included[3]), (1350, 2800), (1750, 2800), (1750, final[1])])
    arrow(pdf, [(3360, additional[3]), (3360, 2800), (2350, 2800), (2350, final[1])])

    pdf.showPage()
    pdf.save()


if __name__ == "__main__":
    create_pdf(OUTPUT)
    print(OUTPUT)
