import os
from fpdf import FPDF
# File creates template of PDF that is created and populated when project is run

# Ensure the ./data target directory exists
os.makedirs("./data", exist_ok=True)

pdf = FPDF()
pdf.add_page()

# Header Title
pdf.set_font("Helvetica", style="B", size=16)
pdf.cell(0, 10, txt="AIED 2026 - Official Conference Guide", ln=1, align="C")

# Subtitle
pdf.set_font("Helvetica", size=10)
pdf.cell(0, 8, txt="Location: Coex Center, Seoul, Republic of Korea | Dates: June 27 - July 3, 2026", ln=1, align="C")
pdf.ln(5)

# Section 1: Theme
pdf.set_font("Helvetica", style="B", size=13)
pdf.cell(0, 8, txt="1. Conference Theme", ln=1)
pdf.set_font("Helvetica", size=10)
pdf.multi_cell(0, 6, txt="Theme: 'From Tools To Teammates: Human-AI Synergy For Augmented Learning'\nAIED 2026 explores how AI evolves from supporting learning tools into adaptive, collaborative teammates for students and educators.")
pdf.ln(4)

# Section 2: Keynotes
pdf.set_font("Helvetica", style="B", size=13)
pdf.cell(0, 8, txt="2. Keynote Speakers", ln=1)
pdf.set_font("Helvetica", size=10)
pdf.multi_cell(0, 6, txt="- Dr. Min-jun Park (Seoul National University): 'Co-evolving with AI Teammates in K-12 Classrooms'\n- Dr. Elena Rostova (ETH Zurich): 'Generative Tutoring Systems & Privacy-First Architecture'")
pdf.ln(4)

# Section 3: Track Locations
pdf.set_font("Helvetica", style="B", size=13)
pdf.cell(0, 8, txt="3. Core Research Tracks & Room Assignments", ln=1)
pdf.set_font("Helvetica", size=10)
pdf.multi_cell(0, 6, txt="- Track 1 (Advances in AI for Learning): Room A1, Hall 3 (Daily @ 10:00 AM)\n- Track 2 (BlueSky Track - Visionary AI): Room B2, Hall 4 (Daily @ 2:00 PM)\n- Track 3 (WideAIED - Global Equity): Room C3, Hall 2 (Daily @ 4:00 PM)")
pdf.ln(4)

# Section 4: Attendee Logistics
pdf.set_font("Helvetica", style="B", size=13)
pdf.cell(0, 8, txt="4. Attendee & Practical Information", ln=1)
pdf.set_font("Helvetica", size=10)
pdf.multi_cell(0, 6, txt="- Wi-Fi Network: AIED2026_Guest (Password: Synergy2026!)\n- Registration & Badge Pick-up: Coex Hall A Lobby, starting June 27 at 08:00 AM\n- Presenter Technical Support & Printing Desk: Coex Hall B, 2nd Floor")

# Save PDF to ./data folder
output_path = "data/aied2026_conference_guide.pdf"
pdf.output(output_path)
print(f"Success! Mock PDF created at: {output_path}")