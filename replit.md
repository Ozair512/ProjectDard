# Project Dard - Replit Configuration

## Overview

Project Dard is a bilingual community discussion platform built with Flask that facilitates academic discussions and knowledge sharing. The platform supports English and Persian (Farsi) languages with RTL text support, featuring weekly topics, stories, community-driven content moderation, and an administrative dashboard.

## System Architecture

### Backend Architecture
- **Framework**: Flask (Python web framework)
- **Database ORM**: SQLAlchemy with Flask-SQLAlchemy
- **Authentication**: Flask-Login for session management
- **Form Handling**: Flask-WTF with WTForms for form validation
- **Security**: Werkzeug for password hashing and proxy handling

### Frontend Architecture
- **Template Engine**: Jinja2 (Flask's default)
- **CSS Framework**: Bootstrap 5 for responsive design
- **Icons**: Font Awesome for UI icons
- **Typography**: Google Fonts (Vazirmatn for Persian text)
- **JavaScript**: Vanilla JavaScript for interactive features

### Database Design
- **Primary Database**: SQLite (development) with PostgreSQL support configured
- **Connection Pooling**: Configured with pool recycling and pre-ping
- **Models**: Admin, WeeklyTopic, WeeklyStory, Comment, CommentVote, Appeal, Visitor

## Key Components

### Authentication System
- Admin-only login system using Flask-Login
- Session-based authentication with remember me functionality
- Password hashing using Werkzeug security utilities

### Content Management
- **Weekly Topics**: Bilingual discussion topics posted by admins
- **Weekly Stories**: Featured stories with author attribution
- **Comments**: User-generated content with voting system
- **Moderation**: Community-driven with like/dislike voting and appeals

### Internationalization
- Built-in translation system supporting English and Persian
- RTL text direction support for Persian content
- Language switching functionality with session persistence

### Admin Dashboard
- Content management for topics and stories
- Comment moderation and appeal review system
- Visitor analytics and statistics tracking
- PDF export functionality for discussions

## Data Flow

1. **User Visit**: Visitor tracking captures IP, user agent, and page data
2. **Content Display**: Language preference determines content display (EN/FA)
3. **User Interaction**: Comments submitted through validated forms
4. **Community Moderation**: Like/dislike system automatically hides heavily disliked comments
5. **Appeal Process**: Users can appeal hidden comments through formal process
6. **Admin Review**: Admins review appeals and manage content through dashboard

## External Dependencies

### Python Packages
- Flask ecosystem (Flask, Flask-SQLAlchemy, Flask-Login, Flask-WTF)
- Database: SQLAlchemy, psycopg2 (for PostgreSQL)
- PDF Generation: ReportLab
- Security: Werkzeug
- Forms: WTForms with validation

### Frontend Libraries
- Bootstrap 5.3.0 (via CDN)
- Font Awesome 6.0.0 (via CDN)
- Google Fonts API (Vazirmatn for Persian)

### Environment Variables
- `DATABASE_URL`: Database connection string
- `SESSION_SECRET`: Flask session secret key

## Deployment Strategy

### Development Setup
- SQLite database for local development
- Debug mode enabled with hot reloading
- Logging configured for debugging

### Production Considerations
- PostgreSQL database support configured
- ProxyFix middleware for reverse proxy deployment
- Session secret from environment variables
- Connection pooling for database efficiency

### Database Migration
- SQLAlchemy model-based table creation
- Automatic table creation on app startup
- Default admin user creation process

## Changelog
- July 01, 2025. Initial setup

## User Preferences

Preferred communication style: Simple, everyday language.