from flask import request, session
from app import db
from models import Visitor

def get_client_ip():
    """Get the client's IP address"""
    if request.environ.get('HTTP_X_FORWARDED_FOR'):
        return request.environ['HTTP_X_FORWARDED_FOR'].split(',')[0].strip()
    elif request.environ.get('HTTP_X_REAL_IP'):
        return request.environ['HTTP_X_REAL_IP']
    else:
        return request.environ.get('REMOTE_ADDR', 'unknown')

def track_visitor():
    """Track visitor statistics"""
    ip_address = get_client_ip()
    user_agent = request.headers.get('User-Agent', '')
    page_visited = request.endpoint or 'unknown'
    
    visitor = Visitor(
        ip_address=ip_address,
        user_agent=user_agent,
        page_visited=page_visited
    )
    
    try:
        db.session.add(visitor)
        db.session.commit()
    except Exception:
        db.session.rollback()

def get_language_direction(language):
    """Get text direction for language"""
    rtl_languages = ['fa', 'ar', 'he', 'ur']
    return 'rtl' if language in rtl_languages else 'ltr'

def format_date(date, language='en'):
    """Format date based on language"""
    if language == 'fa':
        # Persian date formatting would go here
        # For now, return English format
        return date.strftime('%Y/%m/%d')
    else:
        return date.strftime('%B %d, %Y')
