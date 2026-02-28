# from fpdf import FPDF
#
#
# pdf = FPDF()
#
# def create_pdf(file1, file2):
#     pdf.add_page()
#
#     pdf.set_font("Arial", size=12)
#     pdf.cell(200, 10, txt="MINUTES OF MEETING", ln=True)
#
#     pdf.ln(5)
#     pdf.multi_cell(0, 8, "Summary:\n" + file1)
#
#     pdf.ln(5)
#     pdf.multi_cell(0, 8, "Action Items:\n" + "\n".join(file2))
#
#     pdf.output("meeting_minutes.pdf")


def create_pdf(summary, action_items, meeting_title="", meeting_date=None,
               participants=None, decisions=None, questions=None, entities=None):
    """
    Generate a PDF with meeting minutes.

    Args:
        summary (str): Meeting summary
        action_items (list): List of action items
        meeting_title (str): Title of the meeting
        meeting_date (date): Date of the meeting
        participants (list): List of participants
        decisions (list): List of decisions made
        questions (list): List of questions raised
        entities (dict): Dictionary of named entities
    """
    from fpdf import FPDF
    import os
    from datetime import datetime

    # Create a custom PDF class that supports Unicode
    class UnicodePDF(FPDF):
        def __init__(self):
            super().__init__()
            # Add support for Unicode by using a font that supports it
            # You'll need to download a Unicode font like DejaVu or use system font

        def header(self):
            # Skip header for now
            pass

        def footer(self):
            # Skip footer for now
            pass

    # Initialize PDF with Unicode support
    pdf = UnicodePDF()
    pdf.add_page()

    # Try to use a font that supports Unicode
    # Option 1: Use the built-in font with UTF-8 support (might still have issues)
    pdf.set_font("Helvetica", size=12)

    # Option 2: If you have Arial Unicode MS installed, you can use:
    # pdf.add_font('ArialUnicode', '', 'Arial Unicode MS.ttf', uni=True)
    # pdf.set_font('ArialUnicode', '', 12)

    # Set title
    pdf.set_font("Helvetica", 'B', 16)
    pdf.cell(0, 10, "MINUTES OF MEETING", ln=True, align='C')
    pdf.ln(10)

    # Meeting Title and Date
    pdf.set_font("Helvetica", 'B', 12)
    if meeting_title:
        # Replace any problematic characters
        safe_title = meeting_title.encode('latin-1', errors='ignore').decode('latin-1')
        pdf.cell(0, 8, f"Meeting: {safe_title}", ln=True)
    if meeting_date:
        if isinstance(meeting_date, datetime):
            date_str = meeting_date.strftime("%B %d, %Y")
        else:
            date_str = str(meeting_date)
        pdf.cell(0, 8, f"Date: {date_str}", ln=True)
    pdf.ln(5)

    # Participants
    if participants and any(participants):
        pdf.set_font("Helvetica", 'B', 12)
        pdf.cell(0, 8, "Participants:", ln=True)
        pdf.set_font("Helvetica", '', 11)
        for participant in participants:
            if participant:
                # Use hyphen instead of bullet point
                safe_participant = participant.encode('latin-1', errors='ignore').decode('latin-1')
                pdf.cell(0, 6, f"- {safe_participant}", ln=True)
        pdf.ln(5)

    # Summary
    pdf.set_font("Helvetica", 'B', 12)
    pdf.cell(0, 8, "Executive Summary:", ln=True)
    pdf.set_font("Helvetica", '', 11)
    safe_summary = summary.encode('latin-1', errors='ignore').decode('latin-1')
    pdf.multi_cell(0, 6, safe_summary)
    pdf.ln(5)

    # Key Decisions
    if decisions and len(decisions) > 0:
        pdf.set_font("Helvetica", 'B', 12)
        pdf.cell(0, 8, "Key Decisions:", ln=True)
        pdf.set_font("Helvetica", '', 11)
        for i, decision in enumerate(decisions[:5], 1):
            safe_decision = decision.encode('latin-1', errors='ignore').decode('latin-1')
            pdf.multi_cell(0, 6, f"{i}. {safe_decision}")
        pdf.ln(5)

    # Action Items
    if action_items and len(action_items) > 0:
        pdf.set_font("Helvetica", 'B', 12)
        pdf.cell(0, 8, "Action Items:", ln=True)
        pdf.set_font("Helvetica", '', 11)
        for i, item in enumerate(action_items, 1):
            # Clean the item text
            safe_item = item.encode('latin-1', errors='ignore').decode('latin-1')
            pdf.multi_cell(0, 6, f"{i}. {safe_item}")
        pdf.ln(5)

    # Questions
    if questions and len(questions) > 0:
        pdf.set_font("Helvetica", 'B', 12)
        pdf.cell(0, 8, "Questions Raised:", ln=True)
        pdf.set_font("Helvetica", '', 11)
        for i, question in enumerate(questions[:3], 1):
            safe_question = question.encode('latin-1', errors='ignore').decode('latin-1')
            pdf.multi_cell(0, 6, f"{i}. {safe_question}")
        pdf.ln(5)

    # Named Entities
    if entities and any(entities.values()):
        pdf.set_font("Helvetica", 'B', 12)
        pdf.cell(0, 8, "Key Entities Mentioned:", ln=True)
        pdf.set_font("Helvetica", '', 11)

        if entities.get('PERSON'):
            pdf.cell(0, 6, "People:", ln=True)
            for person in entities['PERSON'][:5]:
                safe_person = person.encode('latin-1', errors='ignore').decode('latin-1')
                pdf.cell(0, 5, f"  - {safe_person}", ln=True)

        if entities.get('ORG'):
            pdf.cell(0, 6, "Organizations:", ln=True)
            for org in entities['ORG'][:5]:
                safe_org = org.encode('latin-1', errors='ignore').decode('latin-1')
                pdf.cell(0, 5, f"  - {safe_org}", ln=True)

        if entities.get('DATE'):
            pdf.cell(0, 6, "Dates:", ln=True)
            for date in entities['DATE'][:5]:
                safe_date = date.encode('latin-1', errors='ignore').decode('latin-1')
                pdf.cell(0, 5, f"  - {safe_date}", ln=True)

    # Footer with generation timestamp
    pdf.ln(10)
    pdf.set_font("Helvetica", 'I', 8)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    pdf.cell(0, 5, f"Generated by AI Meeting Minutes Generator on {timestamp}", ln=True, align='C')

    # Generate filename with timestamp
    filename = f"meeting_minutes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf.output(filename)

    return filename