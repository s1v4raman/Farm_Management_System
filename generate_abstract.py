from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generate_abstract():
    doc = SimpleDocTemplate("Project_Abstract.pdf", pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=72)
    
    styles = getSampleStyleSheet()
    
    # Create custom styles
    title_style = styles['Title']
    title_style.fontSize = 18
    title_style.leading = 22
    title_style.spaceAfter = 20
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=12,
        leading=18,
        alignment=4,  # TA_JUSTIFY
        spaceAfter=14
    )
    
    story = []
    
    # Title
    story.append(Paragraph("Project Abstract: Farmer Management System", title_style))
    story.append(Spacer(1, 12))
    
    # Paragraph 1
    p1 = ("The agricultural sector forms the backbone of the economy, yet traditional farm management often "
          "relies on fragmented, manual record-keeping systems that limit operational efficiency and scalability. "
          "The \"Farmer Management System\" aims to bridge this technological gap by providing a comprehensive, "
          "centralized digital platform designed to streamline all facets of modern agricultural operations. "
          "Built utilizing the Django web framework, this web-based application offers a robust suite of tools explicitly "
          "tailored to meet the dynamic needs of farm administrators, employees, and retail consumers.")
    
    # Paragraph 2
    p2 = ("At its core, the system facilitates meticulous record-keeping and data analysis across various farming verticals. "
          "It features dedicated modules for Crop Management—tracking planting, harvesting, daily operations, and localized expenses—as "
          "well as Livestock Management, which intricately monitors the lifecycle and daily production metrics (such as milk and egg yields) of farm animals. "
          "Additionally, the Machinery module ensures the efficient tracking of equipment usage, maintenance schedules, and public renting, "
          "while the Water Management subsystem calculates and tracks irrigation schedules based on crop type and field area, complete with SMS-based alerting capabilities.")
    
    # Paragraph 3
    p3 = ("A key innovation of this platform is its integrated Retail Operations module, which implements secure, role-based access control. "
          "This architecture allows Administrators to securely oversee system health and global sales data, empowers Employees to digitally record retail and farm intake, "
          "and provides a seamless marketplace interface for standard Users to easily purchase farm products including crops, milk, eggs, and machinery rentals. "
          "The system dynamically adapts the user interface according to the user's authenticated role to ensure both simplicity and structural security.")
    
    # Paragraph 4
    p4 = ("Furthermore, the system leverages modern API integrations to provide advanced analytical functionality, including a real-time Daily Climate Tracker, "
          "historical Market Price Analysis, and an AI-driven Crop Recommendation engine that prescribes optimal crops based on soil, season, and water conditions. "
          "By consolidating these diverse operational, financial, and predictive tools into a single, intuitive interface, the Farmer Management System "
          "significantly enhances decision-making capabilities, operational efficiency, and overall productivity for modern farming enterprises.")
    
    story.append(Paragraph(p1, body_style))
    story.append(Paragraph(p2, body_style))
    story.append(Paragraph(p3, body_style))
    story.append(Paragraph(p4, body_style))
    
    doc.build(story)
    print("PDF generated successfully: Project_Abstract.pdf")

if __name__ == '__main__':
    generate_abstract()
