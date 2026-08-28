from pathlib import Path
from xml.etree import ElementTree as ET

from PIL import Image, ImageDraw, ImageFont


ROOT = Path("/Users/annalenz/Desktop/ChronicNoise_Rodents/Prenatal_Chronic_Noise")
OUTPUT = ROOT / "Figures/PCN_PRISMA_flowchart.svg"

WIDTH = 4500
HEIGHT = 3300
FONT_REGULAR = "/System/Library/Fonts/Supplemental/Arial.ttf"
FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"

NAVY = "#17365D"
TEAL = "#13698B"
LIGHT_BLUE = "#D9E8F6"
PALE_BLUE = "#EEF3F7"
PEACH = "#F7D1B0"
PALE_PEACH = "#FBE2D3"
RAIL_TEXT = "#9B4A18"

SVG = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG)

measure_image = Image.new("RGB", (1, 1), "white")
measure_draw = ImageDraw.Draw(measure_image)


def tag(name):
    return f"{{{SVG}}}{name}"


def add_rect(parent, box, fill, stroke=TEAL, stroke_width=7, radius=18):
    x1, y1, x2, y2 = box
    ET.SubElement(parent, tag("rect"), {
        "x": str(x1), "y": str(y1), "width": str(x2 - x1), "height": str(y2 - y1),
        "rx": str(radius), "ry": str(radius), "fill": fill, "stroke": stroke,
        "stroke-width": str(stroke_width), "vector-effect": "non-scaling-stroke",
    })


def wrap_lines(text, font_path, font_size, max_width):
    font = ImageFont.truetype(font_path, font_size)
    lines = []
    for paragraph in text.split("\n"):
        words = paragraph.split()
        if not words:
            lines.append("")
            continue
        current = words[0]
        for word in words[1:]:
            trial = current + " " + word
            if measure_draw.textlength(trial, font=font) <= max_width:
                current = trial
            else:
                lines.append(current)
                current = word
        lines.append(current)
    return lines


def add_centered_text(parent, box, text, font_size, bold=True, color=NAVY, leading=None, pad=34):
    x1, y1, x2, y2 = box
    font_path = FONT_BOLD if bold else FONT_REGULAR
    family = "Arial"
    weight = "700" if bold else "400"
    lines = wrap_lines(text, font_path, font_size, (x2 - x1) - 2 * pad)
    line_height = leading or int(font_size * 1.12)
    start_y = (y1 + y2) / 2 - ((len(lines) - 1) * line_height) / 2
    element = ET.SubElement(parent, tag("text"), {
        "x": str((x1 + x2) / 2), "y": str(start_y), "text-anchor": "middle",
        "dominant-baseline": "middle", "font-family": family, "font-size": str(font_size),
        "font-weight": weight, "fill": color,
    })
    for index, line_text in enumerate(lines):
        tspan = ET.SubElement(element, tag("tspan"), {
            "x": str((x1 + x2) / 2),
            "dy": "0" if index == 0 else str(line_height),
        })
        tspan.text = line_text


def add_left_text(parent, x, y, text, font_size, bold=False, color=NAVY):
    element = ET.SubElement(parent, tag("text"), {
        "x": str(x), "y": str(y), "font-family": "Arial", "font-size": str(font_size),
        "font-weight": "700" if bold else "400", "fill": color,
    })
    element.text = text


def add_line(parent, points, color=TEAL, stroke_width=6):
    ET.SubElement(parent, tag("polyline"), {
        "points": " ".join(f"{px},{py}" for px, py in points),
        "fill": "none", "stroke": color, "stroke-width": str(stroke_width),
        "stroke-linejoin": "round", "stroke-linecap": "round", "vector-effect": "non-scaling-stroke",
    })


def add_arrow(parent, points, color=TEAL, stroke_width=8, head=25):
    add_line(parent, points, color, stroke_width)
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
    ET.SubElement(parent, tag("polygon"), {
        "points": " ".join(f"{px},{py}" for px, py in polygon), "fill": color,
    })


def build_svg(path):
    root = ET.Element(tag("svg"), {
        "width": str(WIDTH), "height": str(HEIGHT), "viewBox": f"0 0 {WIDTH} {HEIGHT}",
        "version": "1.1", "preserveAspectRatio": "xMidYMid meet",
    })
    metadata = ET.SubElement(root, tag("metadata"))
    metadata.text = "Editable vector PRISMA flowchart for the prenatal chronic noise meta-analysis"
    ET.SubElement(root, tag("rect"), {"x": "0", "y": "0", "width": str(WIDTH), "height": str(HEIGHT), "fill": "#FFFFFF"})

    add_rect(root, (270, 65, 4380, 175), LIGHT_BLUE, LIGHT_BLUE, 1, 38)
    add_centered_text(root, (270, 65, 4380, 175), "Records identified from databases and search sources", 52, True, TEAL)

    rails = [
        ((45, 210, 190, 1100), "Identification"),
        ((45, 1140, 190, 2390), "Screening"),
        ((45, 2430, 190, 3210), "Included"),
    ]
    for box, label in rails:
        add_rect(root, box, PEACH, PEACH, 1, 65)
        x1, y1, x2, y2 = box
        cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
        element = ET.SubElement(root, tag("text"), {
            "x": str(cx), "y": str(cy), "text-anchor": "middle", "dominant-baseline": "middle",
            "font-family": "Arial", "font-size": "39", "font-weight": "700", "fill": RAIL_TEXT,
            "transform": f"rotate(-90 {cx} {cy})",
        })
        element.text = label

    top_sources = [
        ((280, 230, 1220, 435), "Scopus\n(n = 1,404)"),
        ((1290, 230, 2230, 435), "Web of Science\n(n = 1,842)"),
        ((2300, 230, 3240, 435), "PubMed\n(n = 1,056)"),
        ((3310, 230, 4250, 435), "PsycINFO\n(n = 408)"),
    ]
    lower_sources = [
        ((350, 520, 1450, 725), "OpenAlex\n(n = 681)"),
        ((1700, 520, 2800, 725), "Google Scholar\nsupplementary search\n(n = 489)"),
        ((3050, 520, 4150, 725), "BASE\n(n = 9)"),
    ]
    for box, text in top_sources + lower_sources:
        add_rect(root, box, "#FFFFFF", TEAL, 7, 4)
        add_centered_text(root, box, text, 40, True, NAVY, 45)

    upper_trunk_y = 475
    upper_centres = []
    for box, _ in top_sources:
        centre = (box[0] + box[2]) / 2
        upper_centres.append(centre)
        add_line(root, [(centre, box[3]), (centre, upper_trunk_y)])
    add_line(root, [(min(upper_centres), upper_trunk_y), (max(upper_centres), upper_trunk_y)])

    merge_x = 1550
    lower_trunk_y = 790
    add_line(root, [(merge_x, upper_trunk_y), (merge_x, lower_trunk_y)])
    lower_centres = []
    for box, _ in lower_sources:
        centre = (box[0] + box[2]) / 2
        lower_centres.append(centre)
        add_line(root, [(centre, box[3]), (centre, lower_trunk_y)])
    add_line(root, [(min(lower_centres), lower_trunk_y), (max(lower_centres), lower_trunk_y)])

    records = (620, 870, 2080, 1050)
    duplicates = (2460, 850, 4260, 1090)
    add_rect(root, records, "#FFFFFF")
    add_centered_text(root, records, "Records identified\n(n = 5,889)", 48)
    add_arrow(root, [(merge_x, lower_trunk_y), (merge_x, 825), (1350, 825), (1350, records[1])])
    add_rect(root, duplicates, PALE_BLUE)
    add_left_text(root, 2510, 930, "Duplicates removed before screening (n = 3,576)", 38, True)
    add_left_text(root, 2510, 995, "Includes duplicate BASE records", 38)
    add_arrow(root, [(records[2], 960), (duplicates[0], 960)])

    unique = (620, 1200, 2080, 1380)
    add_rect(root, unique, "#FFFFFF")
    add_centered_text(root, unique, "Unique records screened\n(n = 2,313)", 48)
    add_arrow(root, [(1350, records[3]), (1350, unique[1])])

    abstract_included = (620, 1540, 2080, 1735)
    add_rect(root, abstract_included, "#FFFFFF")
    add_centered_text(root, abstract_included, "Included at title-and-\nabstract stage\n(n = 87)", 48, True, NAVY, 50)
    add_arrow(root, [(1350, unique[3]), (1350, abstract_included[1])])

    abstract_excluded = (2460, 1515, 4260, 1760)
    add_rect(root, abstract_excluded, PALE_BLUE)
    add_centered_text(root, abstract_excluded, "Records excluded after title-and-abstract screening\n(n = 2,226)", 38, False, NAVY, 43)
    add_arrow(root, [(abstract_included[2], 1638), (abstract_excluded[0], 1638)])

    full_included = (620, 2070, 2080, 2260)
    add_rect(root, full_included, "#FFFFFF")
    add_centered_text(root, full_included, "Included at full-text stage\n(n = 12)", 48, True, NAVY, 52)
    add_arrow(root, [(1350, abstract_included[3]), (1350, full_included[1])])

    full_excluded = (2460, 1940, 4260, 2390)
    add_rect(root, full_excluded, PALE_BLUE)
    add_left_text(root, 2510, 2018, "Full-text reports excluded, with reasons (n = 75)", 38, True)
    reasons = [
        "Wrong exposure (n = 60)", "Wrong outcome (n = 4)", "Wrong publication type (n = 4)",
        "Wrong population (n = 4)", "Foreign language (n = 2)", "Full text not available (n = 1)",
    ]
    for index, reason in enumerate(reasons):
        add_left_text(root, 2510, 2088 + index * 52, reason, 34)
    add_arrow(root, [(full_included[2], 2165), (full_excluded[0], 2165)])

    additional = (2460, 2500, 4260, 2710)
    add_rect(root, additional, PALE_PEACH)
    add_centered_text(root, additional, "Other sources (benchmark set)\n(n = 4)", 48, True, NAVY, 52)

    final = (1150, 2920, 2750, 3150)
    add_rect(root, final, PEACH)
    add_centered_text(root, final, "Studies included in\nthe meta-analysis\n(n = 16)", 48, True, NAVY, 50)
    add_arrow(root, [(1350, full_included[3]), (1350, 2800), (1750, 2800), (1750, final[1])])
    add_arrow(root, [(3360, additional[3]), (3360, 2800), (2350, 2800), (2350, final[1])])

    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ")
    path.parent.mkdir(parents=True, exist_ok=True)
    tree.write(path, encoding="utf-8", xml_declaration=True)


if __name__ == "__main__":
    build_svg(OUTPUT)
    print(OUTPUT)
