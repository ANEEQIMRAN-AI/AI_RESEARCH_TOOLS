# tools.py
from fpdf import FPDF
import re

def format_for_pdf(text):
    lines = text.split("\n")
    formatted_lines = []
    for line in lines:
        clean_line = line.strip()
        if clean_line:
            # Bold numbered headings like 1.1, 2.2 etc.
            if re.match(r"^\d+\.\d+", clean_line):
                formatted_lines.append(("B", clean_line))
            # Bold main headings like ## Heading
            elif clean_line.startswith("##"):
                formatted_lines.append(("B", clean_line.replace("##", "").strip()))
            # Bold **text** style
            elif clean_line.startswith("**") and clean_line.endswith("**"):
                formatted_lines.append(("B", clean_line.replace("**", "").strip()))
            # Handle References heading without asterisks
            elif clean_line.lower().startswith("references"):
                formatted_lines.append(("B", clean_line.replace("*", "").strip()))
            else:
                formatted_lines.append(("", clean_line))
    return formatted_lines

def export_to_pdf(topic: str, content: str, filename: str = None):
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font("Times", "", fname="C:\\Windows\\Fonts\\times.ttf", uni=True)
    pdf.set_font("Times", size=12)

    formatted = format_for_pdf(content)
    for style, line in formatted:
        if style == "B":
            pdf.set_font("Times", "B", 12)
            pdf.multi_cell(0, 7.5, line)
            pdf.set_font("Times", "", 12)
        else:
            pdf.multi_cell(0, 6, line)

    if filename is None:
        filename = topic.strip().replace(" ", "_").replace("/", "-") + ".pdf"
    pdf.output(filename)
    return filename