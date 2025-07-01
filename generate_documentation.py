#!/usr/bin/env python3
"""
Project Dard Documentation Generator
Generates a comprehensive PDF documentation of the entire project
"""

import os
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from datetime import datetime

def read_file_content(filepath):
    """Read file content safely"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

def generate_project_documentation():
    """Generate comprehensive project documentation"""
    
    # Create PDF document
    doc = SimpleDocTemplate(
        "Project_Dard_Documentation.pdf",
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18
    )
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.darkblue,
        spaceAfter=30,
        alignment=1  # Center
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.darkblue,
        spaceAfter=12,
        spaceBefore=20
    )
    
    subheading_style = ParagraphStyle(
        'CustomSubheading',
        parent=styles['Heading3'],
        fontSize=14,
        textColor=colors.darkgreen,
        spaceAfter=6,
        spaceBefore=12
    )
    
    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Code'],
        fontSize=8,
        fontName='Courier',
        leftIndent=20,
        backgroundColor=colors.lightgrey,
        borderColor=colors.black,
        borderWidth=1,
        borderPadding=10
    )
    
    # Story content
    story = []
    
    # Title page
    story.append(Paragraph("Project Dard", title_style))
    story.append(Paragraph("Complete Documentation & Source Code", styles['Heading2']))
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph(f"Generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    
    # Project overview
    story.append(Paragraph("Project Overview", heading_style))
    story.append(Paragraph("""
    Project Dard is a bilingual community discussion platform built with Flask (Python) that facilitates 
    academic discussions and knowledge sharing. The platform supports English and Persian (Farsi) languages 
    with RTL text support, featuring weekly topics, stories, community-driven content moderation, and an 
    administrative dashboard.
    """, styles['Normal']))
    
    # Key features
    story.append(Paragraph("Key Features", subheading_style))
    features = [
        "Bilingual support (English & Persian/Farsi) with RTL text direction",
        "Four main pages: Home, Archive, Info, and Appeal",
        "Community-driven comment system with like/dislike voting",
        "Automatic comment hiding (5 dislikes) with appeal process",
        "Admin dashboard for content management",
        "PDF export functionality for discussions",
        "Dark theme with modern, minimalistic design",
        "Visitor tracking and statistics",
        "Secure admin authentication system"
    ]
    
    for feature in features:
        story.append(Paragraph(f"• {feature}", styles['Normal']))
    
    story.append(PageBreak())
    
    # Technical Stack
    story.append(Paragraph("Technical Stack", heading_style))
    
    tech_data = [
        ['Component', 'Technology'],
        ['Backend Framework', 'Flask (Python)'],
        ['Database ORM', 'SQLAlchemy with Flask-SQLAlchemy'],
        ['Authentication', 'Flask-Login'],
        ['Form Handling', 'Flask-WTF with WTForms'],
        ['Template Engine', 'Jinja2'],
        ['CSS Framework', 'Bootstrap 5'],
        ['Icons', 'Font Awesome 6'],
        ['PDF Generation', 'ReportLab'],
        ['Database', 'SQLite (development) / PostgreSQL (production)'],
        ['Fonts', 'Vazirmatn (Persian), Google Fonts'],
        ['Server', 'Gunicorn WSGI server']
    ]
    
    tech_table = Table(tech_data)
    tech_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(tech_table)
    story.append(PageBreak())
    
    # Project Structure
    story.append(Paragraph("Project Structure", heading_style))
    
    structure = """
    Project Dard/
    ├── app.py                 # Flask application setup and configuration
    ├── main.py               # Application entry point
    ├── models.py             # Database models (Admin, WeeklyTopic, etc.)
    ├── routes.py             # URL routes and view functions
    ├── forms.py              # WTForms form definitions
    ├── utils.py              # Utility functions
    ├── translations.py       # Internationalization support
    ├── templates/            # Jinja2 templates
    │   ├── base.html        # Base template
    │   ├── home.html        # Home page template
    │   ├── archive.html     # Archive page template
    │   ├── info.html        # Info page template
    │   ├── appeal.html      # Appeal page template
    │   └── admin/           # Admin templates
    │       ├── login.html   # Admin login
    │       ├── dashboard.html # Admin dashboard
    │       └── comments.html # Comment management
    ├── static/              # Static assets
    │   ├── css/
    │   │   └── style.css    # Custom CSS styles
    │   ├── js/
    │   │   └── main.js      # JavaScript functionality
    │   └── images/
    │       └── logo.jpg     # Project logo
    ├── pyproject.toml       # Project dependencies
    └── replit.md           # Project documentation
    """
    
    story.append(Preformatted(structure, code_style))
    story.append(PageBreak())
    
    # File contents
    files_to_document = [
        ('app.py', 'Flask Application Setup'),
        ('main.py', 'Application Entry Point'),
        ('models.py', 'Database Models'),
        ('routes.py', 'URL Routes and Views'),
        ('forms.py', 'Form Definitions'),
        ('utils.py', 'Utility Functions'),
        ('translations.py', 'Internationalization'),
        ('templates/base.html', 'Base Template'),
        ('templates/home.html', 'Home Page Template'),
        ('templates/archive.html', 'Archive Page Template'),
        ('templates/info.html', 'Info Page Template'),
        ('templates/appeal.html', 'Appeal Page Template'),
        ('templates/admin/login.html', 'Admin Login Template'),
        ('templates/admin/dashboard.html', 'Admin Dashboard Template'),
        ('templates/admin/comments.html', 'Comment Management Template'),
        ('static/css/style.css', 'CSS Styles'),
        ('static/js/main.js', 'JavaScript Code'),
        ('replit.md', 'Project Documentation')
    ]
    
    for filepath, description in files_to_document:
        story.append(Paragraph(f"{description}", heading_style))
        story.append(Paragraph(f"File: <b>{filepath}</b>", styles['Normal']))
        story.append(Spacer(1, 6))
        
        content = read_file_content(filepath)
        
        # Split content into smaller chunks to avoid ReportLab issues
        lines = content.split('\n')
        chunk_size = 50  # lines per chunk
        
        for i in range(0, len(lines), chunk_size):
            chunk = '\n'.join(lines[i:i+chunk_size])
            if chunk.strip():  # Only add non-empty chunks
                story.append(Preformatted(chunk, code_style))
                story.append(Spacer(1, 6))
        
        story.append(PageBreak())
    
    # Database Schema
    story.append(Paragraph("Database Schema", heading_style))
    
    schema_info = """
    The application uses the following database models:
    
    1. Admin - Administrative users
       - id: Primary key
       - username: Unique username
       - email: Unique email address
       - password_hash: Hashed password
       - created_at: Account creation timestamp
    
    2. WeeklyTopic - Discussion topics
       - id: Primary key
       - title_en/title_fa: Bilingual titles
       - content_en/content_fa: Bilingual content
       - created_at: Creation timestamp
       - is_active: Active status
       - admin_id: Foreign key to Admin
    
    3. WeeklyStory - Featured stories
       - id: Primary key
       - title_en/title_fa: Bilingual titles
       - content_en/content_fa: Bilingual content
       - author_en/author_fa: Bilingual author names
       - created_at: Creation timestamp
       - is_active: Active status
       - admin_id: Foreign key to Admin
    
    4. Comment - User comments
       - id: Primary key
       - content: Comment text
       - language: Comment language ('en' or 'fa')
       - author_name: Commenter name
       - author_email: Commenter email (optional)
       - created_at: Creation timestamp
       - is_hidden: Hidden status
       - likes/dislikes: Vote counts
       - topic_id: Foreign key to WeeklyTopic
    
    5. CommentVote - Vote tracking
       - id: Primary key
       - comment_id: Foreign key to Comment
       - ip_address: Voter IP (to prevent duplicate votes)
       - vote_type: 'like' or 'dislike'
       - created_at: Vote timestamp
    
    6. Appeal - Comment appeals
       - id: Primary key
       - comment_id: Foreign key to Comment
       - appellant_name: Appellant name
       - appellant_email: Appellant email
       - reason: Appeal reason
       - status: 'pending', 'approved', or 'rejected'
       - created_at: Appeal timestamp
       - reviewed_at: Review timestamp
       - admin_id: Foreign key to reviewing Admin
    
    7. Visitor - Analytics
       - id: Primary key
       - ip_address: Visitor IP
       - user_agent: Browser information
       - page_visited: Visited page
       - visited_at: Visit timestamp
    """
    
    story.append(Paragraph(schema_info, styles['Normal']))
    story.append(PageBreak())
    
    # Installation and Setup
    story.append(Paragraph("Installation and Setup", heading_style))
    
    setup_instructions = """
    1. Prerequisites:
       - Python 3.11 or higher
       - pip package manager
    
    2. Install Dependencies:
       pip install flask flask-sqlalchemy flask-login flask-wtf wtforms reportlab psycopg2-binary gunicorn
    
    3. Environment Variables:
       - SESSION_SECRET: Flask session secret key
       - DATABASE_URL: Database connection string (optional, defaults to SQLite)
    
    4. Run Application:
       python main.py
       
       Or using Gunicorn:
       gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app
    
    5. Default Admin Credentials:
       - Username: admin
       - Password: admin123
       (Change these in production!)
    
    6. Access:
       - Main site: http://localhost:5000
       - Admin dashboard: http://localhost:5000/admin
    """
    
    story.append(Paragraph(setup_instructions, styles['Normal']))
    story.append(PageBreak())
    
    # Features and Usage
    story.append(Paragraph("Features and Usage", heading_style))
    
    usage_info = """
    Home Page Features:
    - View current weekly topic and story
    - Post comments in English or Persian
    - Vote on comments (like/dislike)
    - Language switching (EN/FA)
    - Automatic comment hiding (5+ dislikes)
    
    Archive Page:
    - Browse all past discussions
    - Download discussions as PDF
    - Pagination for large datasets
    
    Info Page:
    - Platform information
    - Founder and team bios
    - Featured author spotlight
    - Platform features overview
    
    Appeal Page:
    - Submit appeals for hidden comments
    - Contact information
    - Social media links
    
    Admin Dashboard:
    - Post weekly topics and stories
    - Manage comments (hide/unhide/delete)
    - Review and process appeals
    - View visitor statistics
    - Content moderation tools
    
    Internationalization:
    - Full English and Persian support
    - RTL text direction for Persian
    - Bilingual content management
    - Language-specific date formatting
    """
    
    story.append(Paragraph(usage_info, styles['Normal']))
    
    # Build PDF
    doc.build(story)
    print("Documentation PDF generated successfully: Project_Dard_Documentation.pdf")

if __name__ == "__main__":
    generate_project_documentation()