from datetime import datetime
from app.database.vector_store import VectorStore
from app.services.synthesizer import Synthesizer
from timescale_vector import client
from langfuse.decorators import observe

from app.config.settings import get_settings  # Import the get_settings function
#initialize get_setting for langfuse 
settings = get_settings()
# Initialize VectorStore
vec = VectorStore()

relevant_question = """AMENDMENT NO. 3

Dated as of February 19, 2007

Reference is hereby made to that certain fully executed Wireless Content License Agreement Number 12965 dated as of December 16, 2004, as amended November 11, 2005 and March 27, 2006 (the "Agreement"), between Fox Mobile Entertainment, Inc. ("Fox"), as Administrator for Twentieth Century Fox Film Corporation, and Glu Mobile Inc. ("Licensee").

The parties agree to modify the Agreement as follows:

1. EXTENSION OF TERM: The first paragraph of Section 4 of the Agreement is hereby deleted in its entirety and replaced with the following:

  "TERM: The rights granted hereunder shall be effective as of the Effective Date and shall expire on December 31, 2006 (the "Term"); provided, however, that with respect to each Property, including Robots, Kingdom of Heaven, Mr. and Mrs. Smith, In Her Shoes, Idiocracy (Oww My Balls) and Ice Age II, all right and licenses granted herein will continue in full force and effect until March 31, 2008."

2. NOTICE PROVISION: The notice information for Licensee in Section 17(a) of the Agreement shall be amended such that "Paul Zuzelo" is deleted and replaced with "General Counsel", and such that the email address for Paul Zuzelo is deleted.

Except as herein expressly amended or by necessary implication modified by this Amendment, the Agreement in all other respects is hereby ratified and shall continue in full force and effect.

By signing in the places indicated below, the parties hereto accept and agree to all of the terms and conditions hereof.                   Glu Mobile Inc. ("Licensee")       Fox Mobile Entertainment, Inc. ("Fox")



By:   /s/ Albert A. Pimentel     By:   /s/ Jamie Samson

                  Name:   Albert A. Pimentel       Name:   Jamie Samson Its:   EVP and CFO       Its:   Senior Vice President                   Date:         Date:

Source: GLU MOBILE INC, S-1/A, 3/19/2007"""
results = vec.search(relevant_question, limit=3)

response = Synthesizer.generate_response(question=relevant_question, context=results)

#--------------------------------------------------
#     uncomment this and other part at the end for testing by 
#     running similarity_search.py only
#--------------------------------------------------

# print(f"\n{response.answer}")
# print("\nThought process:")
# for thought in response.thought_process:
#     print(f"- {thought}")
# print(f"\nContext: {response.enough_context}")



from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors

def clean_text(text: str) -> str:
    """
    Cleans the text by removing unwanted characters like ** and -.
    """
    text = text.replace("**", "").replace("- ", "• ")  # Replace - with bullet points
    return text

def convert_to_paragraphs(text: str):
    """
    Converts the cleaned text into a list of formatted Paragraph objects for PDF generation.
    """
    # Clean the text
    cleaned_text = clean_text(text)

    # Create a stylesheet and define custom styles
    styles = getSampleStyleSheet()

    # Check if the style already exists before adding it
    if "Title" not in styles:
        styles.add(ParagraphStyle(
            name="Title",
            fontSize=18,
            fontName="Helvetica-Bold",
            alignment=1,  # Centered
            spaceAfter=20,
        ))
    if "SectionHeader" not in styles:
        styles.add(ParagraphStyle(
            name="SectionHeader",
            fontSize=14,
            fontName="Helvetica-Bold",
            spaceBefore=10,
            spaceAfter=10,
        ))
    if "BodyText" not in styles:
        styles.add(ParagraphStyle(
            name="BodyText",
            fontSize=12,
            leading=15,
            fontName="Helvetica",
            spaceAfter=10,
        ))
    if "BulletText" not in styles:
        styles.add(ParagraphStyle(
            name="BulletText",
            fontSize=12,
            leading=15,
            fontName="Helvetica",
            spaceAfter=6,
            leftIndent=10,
            bulletIndent=0,
            bulletFontName="Helvetica",
            bulletFontSize=12,
        ))

    # Split the text into sections based on headings
    sections = cleaned_text.split("\n\n")
    paragraphs = []

    # Add a title
    paragraphs.append(Paragraph("Compliance Analysis Report", styles["Title"]))
    paragraphs.append(Spacer(1, 0.25 * inch))

    for section in sections:
        if section.strip().startswith("Compliance Report:"):
            paragraphs.append(Paragraph("Compliance Report", styles["SectionHeader"]))
            paragraphs.append(Paragraph(section.strip().split("Compliance Report:")[1].strip(), styles["BodyText"]))
        elif section.strip().startswith("Strengths:"):
            paragraphs.append(Paragraph("Strengths", styles["SectionHeader"]))
            for line in section.strip().split("\n")[1:]:
                paragraphs.append(Paragraph(line.strip(), styles["BulletText"]))
        elif section.strip().startswith("Areas for Improvement:"):
            paragraphs.append(Paragraph("Areas for Improvement", styles["SectionHeader"]))
            for line in section.strip().split("\n")[1:]:
                paragraphs.append(Paragraph(line.strip(), styles["BulletText"]))
        elif section.strip().startswith("Reasoning:"):
            paragraphs.append(Paragraph("Reasoning", styles["SectionHeader"]))
            paragraphs.append(Paragraph(section.strip().split("Reasoning:")[1].strip(), styles["BodyText"]))
        else:
            paragraphs.append(Paragraph(section.strip(), styles["BodyText"]))

        # Add a spacer between sections
        paragraphs.append(Spacer(1, 0.15 * inch))

    return paragraphs

# Example response for testing
response_answer = response.answer

#----------------------------------------------------
#                       uncomment
#----------------------------------------------------

# # Create a beautified PDF
# pdf_filename = "suitability_report.pdf"
# doc = SimpleDocTemplate(
#     pdf_filename,
#     pagesize=letter,
#     rightMargin=0.75 * inch,
#     leftMargin=0.75 * inch,
#     topMargin=1 * inch,
#     bottomMargin=0.75 * inch,
# )

# Convert the string into styled paragraphs
paragraphs = convert_to_paragraphs(response_answer)

#-------------------------------------------------
#  UNCOMMENT
#  # Build the beautified PDF
# doc.build(paragraphs)

# print(f"Beautified PDF generated: {pdf_filename}")





# --------------------------------------------------------------
# Irrelevant question
# --------------------------------------------------------------

# irrelevant_question = "What is the weather in Tokyo?"

# results = vec.search(irrelevant_question, limit=3)

# response = Synthesizer.generate_response(question=irrelevant_question, context=results)

# print(f"\n{response.answer}")
# print("\nThought process:")
# for thought in response.thought_process:
#     print(f"- {thought}")
# print(f"\nContext: {response.enough_context}")

# --------------------------------------------------------------
# Metadata filtering
# --------------------------------------------------------------

# metadata_filter = {"Category": "PHP Developer"}

# results = vec.search(relevant_question, limit=3, metadata_filter=metadata_filter)

# response = Synthesizer.generate_response(question=relevant_question, context=results)

# print(f"\n{response.answer}")
# print("\nThought process:")
# for thought in response.thought_process:
#     print(f"- {thought}")
# print(f"\nContext: {response.enough_context}")

# --------------------------------------------------------------
# Advanced filtering using Predicates
# --------------------------------------------------------------

# predicates = client.Predicates("category", "==", "Shipping")
# results = vec.search(relevant_question, limit=3, predicates=predicates)


# predicates = client.Predicates("category", "==", "Shipping") | client.Predicates(
#     "category", "==", "Services"
# )
# results = vec.search(relevant_question, limit=3, predicates=predicates)


# predicates = client.Predicates("category", "==", "Shipping") & client.Predicates(
#     "created_at", ">", "2024-09-01"
# )
# results = vec.search(relevant_question, limit=3, predicates=predicates)

# # --------------------------------------------------------------
# # Time-based filtering
# # --------------------------------------------------------------

# # September — Returning results
# time_range = (datetime(2024, 9, 1), datetime(2024, 9, 30))
# results = vec.search(relevant_question, limit=3, time_range=time_range)

# # August — Not returning any results
# time_range = (datetime(2024, 8, 1), datetime(2024, 8, 30))
# results = vec.search(relevant_question, limit=3, time_range=time_range)
