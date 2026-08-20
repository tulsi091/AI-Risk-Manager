import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.colors import HexColor


def create_pdf(company, industry, analysis):

    os.makedirs("reports", exist_ok=True)

    filename = f"reports/{company}_Risk_Report.pdf"

    doc = SimpleDocTemplate(filename, pagesize=letter)

    styles = getSampleStyleSheet()

    title_style = styles["Title"]
    title_style.alignment = TA_CENTER
    title_style.textColor = HexColor("#0B5394")

    heading = styles["Heading2"]
    heading.textColor = HexColor("#1F4E79")

    normal = styles["BodyText"]

    story = []

    story.append(Paragraph("AI Risk Assessment Report", title_style))
    story.append(Spacer(1, 20))

    story.append(Paragraph(f"<b>Company:</b> {company}", normal))
    story.append(Paragraph(f"<b>Industry:</b> {industry}", normal))

    story.append(Spacer(1, 20))

    story.append(Paragraph("AI Generated Risk Analysis", heading))

    story.append(Spacer(1, 10))

    for line in analysis.split("\n"):

        if line.strip():

            story.append(Paragraph(line, normal))

    doc.build(story)

    return filename