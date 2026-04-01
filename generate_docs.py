import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def create_base_paper():
    doc = SimpleDocTemplate("Base_Paper.pdf", pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=72)
    styles = getSampleStyleSheet()
    
    title_style = styles['Title']
    title_style.fontSize = 18
    title_style.spaceAfter = 20
    
    heading_style = styles['Heading2']
    heading_style.spaceBefore = 16
    heading_style.spaceAfter = 10
    
    body_style = ParagraphStyle('CustomBody', parent=styles['Normal'], fontSize=11, leading=16, alignment=4, spaceAfter=12)
    
    story = []
    
    story.append(Paragraph("Farmer Management System: A Comprehensive Digital Platform for Modern Agriculture", title_style))
    story.append(Paragraph("Abstract", heading_style))
    story.append(Paragraph("Traditional agricultural management relies heavily on fragmented, manual record-keeping, leading to inefficiencies, reduced profitability, and a high margin for error in critical farm operations. This paper presents the 'Farmer Management System,' a centralized digital web application built on the Django framework designed to solve these exact problems. The system comprehensively integrates modules for Crop Management, Livestock Tracking, Machinery Renting, Water Scheduling, and Retail Operations into a single, cohesive platform. Furthermore, it leverages AI-driven crop recommendations and external APIs for real-time weather tracking and market price analysis, empowering farmers with actionable intelligence. The platform implements robust role-based access control (Admin, Employee, User) to ensure data security, privacy, and operational accountability across different user tiers. Our results indicate that digitizing these workflows and integrating them with predictive analytics heavily streamlines farm operations, reduces overhead costs, and enhances data-driven decision-making in the agricultural sector. Ultimately, this system aims to bridge the gap between traditional farming practices and the technological advancements of the 21st century.", body_style))
    
    story.append(Paragraph("1. Introduction", heading_style))
    story.append(Paragraph("Agriculture remains the primary source of livelihood for millions globally and forms the backbone of the world's economy. However, despite its critical importance, the lack of centralized and accessible management tools forces many farm administrators to use disjointed systems to track their resources, finances, and day-to-day operations. This often results in data silos, where crucial information regarding crop yields, livestock health, and machinery utilization is lost or mismanaged. Modern agriculture requires precision, driven by accurate, real-time data.", body_style))
    story.append(Paragraph("The Farmer Management System (FMS) addresses these systemic challenges by offering an all-in-one solution that integrates financial tracking, resource management, and retail sales workflows. By transitioning from traditional pen-and-paper or disconnected spreadsheet methods to a unified digital ecosystem, farmers can gain unprecedented visibility into their entire operation. This system allows for proactive rather than reactive management, facilitating better resource allocation, enhanced crop planning, and streamlined coordination between farm hands, administration, and end consumers.", body_style))
    story.append(Paragraph("Furthermore, the increasing unpredictability of global climate patterns and the volatility of agricultural commodity markets necessitate advanced predictive tools. The FMS integrates directly with cutting-edge Machine Learning models to offer recommendations that are tailored to hyper-local environmental conditions, transforming traditional farming from an intuition-based practice to a modern, data-driven science.", body_style))
    
    story.append(Paragraph("2. Literature Review", heading_style))
    story.append(Paragraph("Previous attempts at farm management software have frequently focused on single verticals or niche problems within the agricultural space. For instance, many existing applications offer standalone solutions such as only tracking expenses, only providing weather updates, or strictly focusing on yield prediction. While these tools are individually useful, research shows a prominent gap in integrated systems that handle both the production side (like planting, harvesting, and livestock care) and the business side (like direct-to-consumer retail sales, machinery renting, and localized economic tracking).", body_style))
    story.append(Paragraph("Current literature indicates that farmers suffer from 'app fatigue' when required to manage multiple disjointed software platforms. This fatigue often leads to inconsistent data entry, thereby negating the benefits of digitization. This system builds upon recent advancements in full-stack web technologies and predictive artificial intelligence to offer a holistic approach. By centralizing operations, the proposed FMS mitigates this issue directly. Furthermore, existing literature emphasizes the necessity of Role-Based Access Control in multi-user agricultural platforms to prevent unauthorized data manipulation, a feature that the FMS incorporates fundamentally into its architecture from the ground up.", body_style))
    story.append(Paragraph("Recent studies also highlight the importance of integrating direct-to-consumer sales channels into farm management software. By bypassing traditional supply chains, farmers can realize significantly higher profit margins. The FMS's Retail Operations module is directly informed by this research, providing a seamless marketplace interface integrated right alongside production tracking.", body_style))
    
    story.append(Paragraph("3. Methodology", heading_style))
    story.append(Paragraph("The system is developed using the Django Web Framework, a high-level Python framework chosen for its rapid development capabilities, built-in ORM, and deeply integrated security features. It leverages an SQLite database for reliable data persistence during operation, and utilizes modern HTML, CSS, and JavaScript for an intuitive and responsive frontend user experience featuring 'glassmorphic' design principles for enhanced usability. The architecture is intentionally modular, allowing for future expansion. The core components include:", body_style))
    story.append(Paragraph("- <b>Crop & Livestock Modules:</b> Detailed tracking interfaces for planting/harvesting cycles, operational expenses, medication logs, and daily yields (such as milk and eggs). This allows for granular profitability analysis per crop or animal.<br/>"
                           "- <b>Water Management:</b> A specialized module that calculates precise irrigation times based on specific crop requirements, field area, and water pump flow rates, featuring an integrated SMS alert mechanism to notify staff when watering is complete.<br/>"
                           "- <b>Retail Operations:</b> A built-in customized marketplace where administrators can easily manage product inventory and pricing, and where standard users can seamlessly browse and purchase farm-fresh goods directly, cutting out middlemen.<br/>"
                           "- <b>AI & API Integrations:</b> The integration of predictive machine learning models for crop recommendations based on soil parameters and climate conditions, alongside real-time weather API integration and mathematical trend analysis for past market prices.", body_style))
    story.append(Paragraph("The development lifecycle followed an Agile methodology, beginning with extensive requirement gathering regarding the specific pain points of modern farm administrators. Subsequent phases included iterative database schema design, backend logic implementation, and finally frontend aesthetic polishing to ensure the system remained accessible to users with varying levels of technical literacy.", body_style))

    story.append(Paragraph("4. Role-Based Security Architecture", heading_style))
    story.append(Paragraph("Data security, privacy, and operational integrity are maintained via a strict 3-tier hierarchy built directly into the authentication layer, utilizing Django's internal User and Group management models: <br/>"
                           "- <b>Admin:</b> Administrators possess full Create, Read, Update, and Delete (CRUD) access and global visibility across the entire system. They manage inventory, oversee employee actions, configure system-wide settings, and handle financial audits.<br/>"
                           "- <b>Employee:</b> Staff members are granted the ability to view necessary operational data and add daily logs (e.g., milk yields) or record retail sales, but they are critically restricted from editing or deleting historical data, preventing tampering or accidental data loss.<br/>"
                           "- <b>User:</b> Designed purely for public consumers, this access level restricts users exclusively to the retail frontend, allowing them to browse available inventory, make purchases, and manage their own profiles without accessing any backend farm data.", body_style))
    
    story.append(Paragraph("5. System Advantages and Impact", heading_style))
    story.append(Paragraph("The deployment of the Farmer Management System introduces several distinct advantages over traditional operations. Firstly, it heavily reduces administrative overhead by automating routine calculations, such as irrigation timing and profit margin analysis. This automation frees up valuable man-hours that can be redirected towards active farm labor or strategic planning. Secondly, it fosters a direct-to-consumer sales channel which significantly improves the economic viability of small-to-medium scale farms by eliminating third-party retail markups.", body_style))
    story.append(Paragraph("Furthermore, the inclusion of AI recommendations ensures that cropping decisions are made based on empirical data rather than solely on historical precedent or intuition, mitigating the risks associated with changing climate patterns and soil degradation. The centralized nature of the platform also drastically improves communication between different tiers of farm staff, ensuring everyone is operating off the same, up-to-date data set.", body_style))
    
    story.append(Paragraph("6. Future Scope", heading_style))
    story.append(Paragraph("While the current iteration of the FMS provides a robust foundation, future expansions will seek to integrate direct IoT (Internet of Things) sensor data for automated soil moisture tracking, effectively closing the loop in the Water Management module without requiring manual field measurements. Additionally, blockchain integration for verifiable supply chain tracking from 'farm to table' is currently under feasibility review.", body_style))

    story.append(Paragraph("7. Conclusion", heading_style))
    story.append(Paragraph("The Farmer Management System conclusively proves that consolidating diverse agricultural workflows into a single, well-architected digital platform drastically improves operational efficiency. By combining day-to-day operational tracking with advanced market and weather intelligence, farmers are empowered to make sustainable, profit-maximizing decisions in real-time. As agriculture continues to modernize, comprehensive systems like the FMS will become essential infrastructure for maintaining profitability and sustainability in an increasingly competitive global market. The successful implementation of this system marks a significant step forward in the digital transformation of agricultural management.", body_style))

    
    doc.build(story)


def create_timeline():
    doc = SimpleDocTemplate("Project_Timeline.pdf", pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=72)
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    
    story = []
    story.append(Paragraph("Project Timeline: November 2025 - January 2026", title_style))
    story.append(Spacer(1, 20))
    
    data = [
        ["Month", "Week", "Key Activities / Milestones"],
        
        ["November 2025", "Week 1-2", "Requirement Gathering & Feasibility Study\nDefining core modules (Crops, Livestock, Retail)."],
        ["", "Week 3", "Database Architecture & Schema Design\nStructuring tables for Roles, Sales, Production."],
        ["", "Week 4", "UI/UX Design & Prototyping\nDesigning Dashboard, Login/Registration forms."],
        
        ["December 2025", "Week 1-2", "Backend Development (Django)\nBuilding Models, Views, Authentication logic."],
        ["", "Week 3", "API Integrations & ML\nImplementing Weather API, Crop AI, Market logic."],
        ["", "Week 4", "Retail Module & Access Control\nAssigning Admin/Employee/User permissions."],
        
        ["January 2026", "Week 1-2", "Frontend Integration & Visuals\nConnecting templates, styling glassmorphism UI."],
        ["", "Week 3", "System Testing & Debugging\nResolving lint errors, securing edit/delete routes."],
        ["", "Week 4", "Final Documentation & Deployment\nAbstract generation, Base Paper formulation, Handover."]
    ]
    
    table = Table(data, colWidths=[90, 70, 300])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#2c3e50")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 12),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor("#ecf0f1")),
        ('TEXTCOLOR', (0,1), (-1,-1), colors.black),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,1), (-1,-1), 10),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    
    story.append(table)
    doc.build(story)

def create_crop_records_report():
    doc = SimpleDocTemplate("Crop_Records_Module_Report.pdf", pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=72)
    styles = getSampleStyleSheet()
    
    title_style = styles['Title']
    
    heading_style = styles['Heading2']
    heading_style.spaceBefore = 16
    heading_style.spaceAfter = 10
    
    body_style = ParagraphStyle('CustomBody', parent=styles['Normal'], fontSize=11, leading=16, spaceAfter=12)
    
    story = []
    
    story.append(Paragraph("Crop Records Module - Full Explanation", title_style))
    
    story.append(Paragraph("1. Purpose of the Module", heading_style))
    story.append(Paragraph("The Crop Records module is used to store, manage, and track all crop-related information for each farmer. It helps farmers and administrators keep a digital record of agricultural activities.", body_style))
    
    story.append(Paragraph("2. What You See in the Screen", heading_style))
    story.append(Paragraph("<b>Header: Crop Records</b><br/>Displays the module name. Usually part of the dashboard navigation.<br/><br/>"
                           "<b>'Add Crop' Button (Top Right)</b><br/>Used to add a new crop entry. Redirects to a form where users input crop details.<br/><br/>"
                           "<b>Empty State Message</b><br/>'No crops found. Add your first crop to get started.' This appears when the database has no crop records. Improves user experience by guiding the next action.<br/><br/>"
                           "<b>Center 'Add Crop' Button</b><br/>Same function as the top button. Designed for easy access when there are no records.", body_style))
    
    story.append(Paragraph("3. Features of Crop Records Module", heading_style))
    story.append(Paragraph("<b>Add Crop:</b> User can enter Crop Name (e.g., Rice, Wheat), Season (Kharif/Rabi), Sowing Date, Harvest Date, Quantity Produced, Cost & Profit, Field Location.<br/><br/>"
                           "<b>View Crop Records:</b> Displays all added crops in table or card format. Shows details like Crop Name, Dates, Yield, Status.<br/><br/>"
                           "<b>Edit Crop:</b> Update existing crop details. Useful when Yield changes or Harvest date updated.<br/><br/>"
                           "<b>Delete Crop:</b> Remove incorrect or outdated records.", body_style))

    story.append(Paragraph("4. Backend Functionality (Django)", heading_style))
    story.append(Paragraph("<b>Model Example:</b><br/>"
                           "class Crop(models.Model):<br/>"
                           "&nbsp;&nbsp;&nbsp;&nbsp;name = models.CharField(max_length=100)<br/>"
                           "&nbsp;&nbsp;&nbsp;&nbsp;season = models.CharField(max_length=50)<br/>"
                           "&nbsp;&nbsp;&nbsp;&nbsp;sowing_date = models.DateField()<br/>"
                           "&nbsp;&nbsp;&nbsp;&nbsp;harvest_date = models.DateField()<br/>"
                           "&nbsp;&nbsp;&nbsp;&nbsp;quantity = models.FloatField()<br/>"
                           "&nbsp;&nbsp;&nbsp;&nbsp;cost = models.FloatField()<br/>"
                           "&nbsp;&nbsp;&nbsp;&nbsp;profit = models.FloatField()<br/>"
                           "<br/><b>Views:</b><br/>"
                           "add_crop() → Handles form submission<br/>"
                           "crop_list() → Fetch and display crops<br/>"
                           "update_crop() → Edit data<br/>"
                           "delete_crop() → Remove data<br/>"
                           "<br/><b>Template Behavior:</b><br/>"
                           "If no data: {% if not crops %} &lt;p&gt;No crops found&lt;/p&gt; {% endif %}", body_style))
    
    story.append(Paragraph("5. Importance of This Module", heading_style))
    story.append(Paragraph("📊 Helps in data-driven farming decisions<br/>"
                           "💰 Tracks profit and loss<br/>"
                           "📅 Maintains crop history<br/>"
                           "📈 Useful for prediction & analytics (future scope)", body_style))

    story.append(Paragraph("6. Future Enhancements (Good for Viva 💡)", heading_style))
    story.append(Paragraph("You can improve this module by adding:<br/>"
                           "📊 Crop yield prediction (Machine Learning)<br/>"
                           "🌦 Weather integration<br/>"
                           "📍 GPS-based farm mapping<br/>"
                           "📉 Analytics dashboard (charts)<br/>"
                           "📄 PDF report generation", body_style))
    
    story.append(Paragraph("7. Real-Time Use Case", heading_style))
    story.append(Paragraph("A farmer: Logs into the system, clicks Add Crop, enters crop details, tracks growth and harvest, views profit analysis.", body_style))
    
    story.append(Paragraph("Summary", heading_style))
    story.append(Paragraph("The Crop Records module is the core component of the Farmer Management System that digitizes agricultural data, improves tracking, and supports smarter farming decisions.", body_style))

    story.append(Spacer(1, 20))
    story.append(Paragraph("Financial & Activity Tracking Module - Full Explanation", title_style))
    
    story.append(Paragraph("1. Crop Expenses Module", heading_style))
    story.append(Paragraph("<b>Purpose:</b> This module is used to record all expenses incurred during crop cultivation. It helps farmers track how much money is spent.", body_style))
    story.append(Paragraph("<b>Fields Explanation:</b><br/>"
                           "<b>Expense Date:</b> Date when the expense occurred.<br/>"
                           "<b>Type:</b> Category of expense (Seeds, Fertilizer, Labor, Transport, Equipment, etc.).<br/>"
                           "<b>Description:</b> Detailed explanation of expense.<br/>"
                           "<b>Budget:</b> Planned cost (expected amount).<br/>"
                           "<b>Amount:</b> Actual money spent.<br/>"
                           "<b>Supplier:</b> From whom items/services were purchased.<br/>"
                           "<b>Payment:</b> Payment method (Cash, UPI, Bank Transfer).<br/>"
                           "<b>Receipt #:</b> Invoice or receipt number for record.", body_style))
    story.append(Paragraph("<b>Importance:</b> Tracks total investment, helps in cost analysis, and is useful for profit calculation.", body_style))

    story.append(Paragraph("2. Crop Sales Module", heading_style))
    story.append(Paragraph("<b>Purpose:</b> This module records all crop selling transactions. It helps farmers track income and revenue.", body_style))
    story.append(Paragraph("<b>Fields Explanation:</b><br/>"
                           "<b>Sale Date:</b> Date of selling crop.<br/>"
                           "<b>Qty Sold:</b> Quantity sold (kg, tons, etc.).<br/>"
                           "<b>Unit Price:</b> Price per unit.<br/>"
                           "<b>Total Price:</b> Auto-calculated (Qty × Price).<br/>"
                           "<b>Buyer Info:</b> Customer name or market.<br/>"
                           "<b>Payment:</b> Mode of payment.<br/>"
                           "<b>Status:</b> Paid / Pending / Partial.<br/>"
                           "<b>Invoice #:</b> Invoice reference.<br/>"
                           "<b>Notes:</b> Additional details.", body_style))
    story.append(Paragraph("<b>Importance:</b> Tracks income generation, helps calculate profit/loss, and maintains sales history.", body_style))

    story.append(Paragraph("3. Crop Operations Module", heading_style))
    story.append(Paragraph("<b>Purpose:</b> This module tracks day-to-day farming activities performed on crops.", body_style))
    story.append(Paragraph("<b>Fields Explanation:</b><br/>"
                           "<b>Operation Date:</b> Date of activity.<br/>"
                           "<b>Operation Name:</b> Type of work (Plowing, Irrigation, Fertilizing, Spraying, Harvesting).<br/>"
                           "<b>Additional Notes:</b> Extra details about the operation.", body_style))
    story.append(Paragraph("<b>Importance:</b> Maintains activity log, helps monitor crop lifecycle, and is useful for future planning.", body_style))

    story.append(Paragraph("4. How These Modules Work Together", heading_style))
    story.append(Paragraph("<b>Flow of Data:</b><br/>"
                           "Crop Created → (Crop Records Module)<br/>"
                           "Expenses Added → Money spent on crop<br/>"
                           "Operations Logged → Daily farming activities<br/>"
                           "Sales Recorded → Income generated<br/><br/>"
                           "<b>Profit Calculation Logic:</b> Profit = Total Sales - Total Expenses", body_style))
    
    story.append(Paragraph("5. Backend Design (Django Models)", heading_style))
    story.append(Paragraph("<b>Expense Model:</b><br/>"
                           "class Expense(models.Model):<br/>"
                           "&nbsp;&nbsp;&nbsp;&nbsp;date = models.DateField()<br/>"
                           "&nbsp;&nbsp;&nbsp;&nbsp;type = models.CharField(max_length=100)<br/>"
                           "&nbsp;&nbsp;&nbsp;&nbsp;description = models.TextField()<br/>"
                           "&nbsp;&nbsp;&nbsp;&nbsp;budget = models.FloatField()<br/>"
                           "&nbsp;&nbsp;&nbsp;&nbsp;amount = models.FloatField()<br/>"
                           "&nbsp;&nbsp;&nbsp;&nbsp;supplier = models.CharField(max_length=100)<br/>"
                           "&nbsp;&nbsp;&nbsp;&nbsp;payment = models.CharField(max_length=50)<br/>"
                           "&nbsp;&nbsp;&nbsp;&nbsp;receipt_no = models.CharField(max_length=50)<br/><br/>"
                           "<b>Sales Model:</b><br/>"
                           "class Sale(models.Model):<br/>"
                           "&nbsp;&nbsp;&nbsp;&nbsp;sale_date = models.DateField()<br/>"
                           "&nbsp;&nbsp;&nbsp;&nbsp;quantity = models.FloatField()<br/>"
                           "&nbsp;&nbsp;&nbsp;&nbsp;unit_price = models.FloatField()<br/>"
                           "&nbsp;&nbsp;&nbsp;&nbsp;total_price = models.FloatField()<br/>"
                           "&nbsp;&nbsp;&nbsp;&nbsp;buyer = models.CharField(max_length=100)<br/>"
                           "&nbsp;&nbsp;&nbsp;&nbsp;payment = models.CharField(max_length=50)<br/>"
                           "&nbsp;&nbsp;&nbsp;&nbsp;status = models.CharField(max_length=50)<br/>"
                           "&nbsp;&nbsp;&nbsp;&nbsp;invoice_no = models.CharField(max_length=50)<br/>"
                           "&nbsp;&nbsp;&nbsp;&nbsp;notes = models.TextField()<br/><br/>"
                           "<b>Operations Model:</b><br/>"
                           "class Operation(models.Model):<br/>"
                           "&nbsp;&nbsp;&nbsp;&nbsp;operation_date = models.DateField()<br/>"
                           "&nbsp;&nbsp;&nbsp;&nbsp;operation_name = models.CharField(max_length=100)<br/>"
                           "&nbsp;&nbsp;&nbsp;&nbsp;notes = models.TextField()", body_style))

    story.append(Paragraph("6. Advanced Features (For High Marks 💡)", heading_style))
    story.append(Paragraph("You can enhance your project with:<br/>"
                           "📊 Dashboard charts (Expenses vs Sales)<br/>"
                           "📉 Profit/Loss analytics<br/>"
                           "📅 Calendar view of operations<br/>"
                           "📄 PDF invoice generation<br/>"
                           "🔔 Payment reminders<br/>"
                           "🤖 AI-based cost prediction", body_style))
                           
    story.append(Paragraph("Final Summary", heading_style))
    story.append(Paragraph("Together, the Crop Expenses (Track money spent), Crop Sales (Track income), and Crop Operations (Track activities) modules help farmers monitor farming performance, manage finances, and make better decisions.", body_style))
    
    doc.build(story)

if __name__ == "__main__":
    create_base_paper()
    create_timeline()
    create_crop_records_report()
    print("Documents generated successfully.")
