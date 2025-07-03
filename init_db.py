#!/usr/bin/env python3
"""
Initialize the database with default admin user
"""

from app import app, db
from models import Admin
from werkzeug.security import generate_password_hash

def init_database():
    """Initialize database with default admin user"""
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Check if admin user already exists
        existing_admin = Admin.query.filter_by(username='admin').first()
        if existing_admin:
            print("Admin user already exists!")
            return
        
        # Create default admin user
        admin = Admin(
            username='admin',
            email='admin@projectdard.com',
            password_hash=generate_password_hash('admin123')
        )
        
        db.session.add(admin)
        db.session.commit()
        
        print("Database initialized successfully!")
        print("Default admin credentials:")
        print("Username: admin")
        print("Password: admin123")

if __name__ == "__main__":
    init_database()