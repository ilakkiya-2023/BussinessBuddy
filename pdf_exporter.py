from fpdf import FPDF

def generate_pdf(content):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # Set title
    pdf.set_font("Arial", size=12, style='B')
    pdf.cell(200, 10, txt="BusinessBuddy Report", ln=True, align='C')
    
    # Add content
    pdf.set_font("Arial", size=10)
    for line in content:
        pdf.multi_cell(0, 10, line)
    
    # Return as buffer
    buffer = pdf.output(dest='S').encode('latin1')
    return buffer
