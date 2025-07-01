from datetime import datetime
from app import db
from flask_login import UserMixin

class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class WeeklyTopic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title_en = db.Column(db.Text, nullable=False)
    title_fa = db.Column(db.Text)
    content_en = db.Column(db.Text, nullable=False)
    content_fa = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)
    
    comments = db.relationship('Comment', backref='topic', lazy=True)

class WeeklyStory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title_en = db.Column(db.Text, nullable=False)
    title_fa = db.Column(db.Text)
    content_en = db.Column(db.Text, nullable=False)
    content_fa = db.Column(db.Text)
    author_en = db.Column(db.String(100))
    author_fa = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    language = db.Column(db.String(2), default='en')  # 'en' or 'fa'
    author_name = db.Column(db.String(100), nullable=False)
    author_email = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_hidden = db.Column(db.Boolean, default=False)
    likes = db.Column(db.Integer, default=0)
    dislikes = db.Column(db.Integer, default=0)
    topic_id = db.Column(db.Integer, db.ForeignKey('weekly_topic.id'), nullable=False)
    
    votes = db.relationship('CommentVote', backref='comment', lazy=True)
    appeals = db.relationship('Appeal', backref='comment', lazy=True)

class CommentVote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'), nullable=False)
    ip_address = db.Column(db.String(45), nullable=False)  # Support IPv6
    vote_type = db.Column(db.String(10), nullable=False)  # 'like' or 'dislike'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('comment_id', 'ip_address'),)

class Appeal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'), nullable=False)
    appellant_name = db.Column(db.String(100), nullable=False)
    appellant_email = db.Column(db.String(120), nullable=False)
    reason = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='pending')  # 'pending', 'approved', 'rejected'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    reviewed_at = db.Column(db.DateTime)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))

class Visitor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(45), nullable=False)
    user_agent = db.Column(db.Text)
    page_visited = db.Column(db.String(100))
    visited_at = db.Column(db.DateTime, default=datetime.utcnow)
