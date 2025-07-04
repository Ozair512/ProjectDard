import os
from datetime import datetime
from flask import render_template, request, redirect, url_for, flash, session, jsonify, make_response
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

from app import app, db
from models import Admin, WeeklyTopic, WeeklyStory, Comment, CommentVote, Appeal, Visitor
from forms import LoginForm, CommentForm, WeeklyTopicForm, WeeklyStoryForm, AppealForm
from utils import get_client_ip, track_visitor
from translations import get_text, get_supported_languages

@app.before_request
def before_request():
    # Set default language
    if 'language' not in session:
        session['language'] = 'en'
    
    # Track visitor
    track_visitor()

@app.context_processor
def inject_globals():
    return {
        'get_text': get_text,
        'current_language': session.get('language', 'en'),
        'supported_languages': get_supported_languages()
    }

@app.route('/', methods=['GET', 'POST'])
def home():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    # Get active topic
    active_topic = WeeklyTopic.query.filter_by(is_active=True).order_by(WeeklyTopic.created_at.desc()).first()
    
    # Get active story
    active_story = WeeklyStory.query.filter_by(is_active=True).order_by(WeeklyStory.created_at.desc()).first()
    
    # Get comments for active topic
    comments = None
    if active_topic:
        comments = Comment.query.filter_by(topic_id=active_topic.id, is_hidden=False)\
                               .order_by(Comment.created_at.desc())\
                               .paginate(page=page, per_page=per_page, error_out=False)
    
    # Comment form
    form = CommentForm()
    if form.validate_on_submit() and active_topic:
        comment = Comment(
            content=form.content.data,
            language=form.language.data,
            author_name=form.author_name.data,
            author_email=form.author_email.data,
            topic_id=active_topic.id
        )
        db.session.add(comment)
        db.session.commit()
        
        # Update Excel with latest data
        try:
            from excel_manager import excel_manager
            excel_manager.export_all_data()
        except Exception as e:
            print(f"Excel export error: {e}")
        
        flash(get_text('comment_posted'), 'success')
        return redirect(url_for('home'))
    
    return render_template('home.html', 
                         active_topic=active_topic, 
                         active_story=active_story,
                         comments=comments, 
                         form=form)

@app.route('/vote_comment/<int:comment_id>/<vote_type>')
def vote_comment(comment_id, vote_type):
    if vote_type not in ['like', 'dislike']:
        return jsonify({'error': 'Invalid vote type'}), 400
    
    comment = Comment.query.get_or_404(comment_id)
    ip_address = get_client_ip()
    
    # Check if user already voted
    existing_vote = CommentVote.query.filter_by(comment_id=comment_id, ip_address=ip_address).first()
    
    if existing_vote:
        if existing_vote.vote_type == vote_type:
            # Remove vote
            db.session.delete(existing_vote)
            if vote_type == 'like':
                comment.likes -= 1
            else:
                comment.dislikes -= 1
        else:
            # Change vote
            existing_vote.vote_type = vote_type
            if vote_type == 'like':
                comment.likes += 1
                comment.dislikes -= 1
            else:
                comment.dislikes += 1
                comment.likes -= 1
    else:
        # New vote
        vote = CommentVote(comment_id=comment_id, ip_address=ip_address, vote_type=vote_type)
        db.session.add(vote)
        if vote_type == 'like':
            comment.likes += 1
        else:
            comment.dislikes += 1
    
    # Auto-hide comment if it has 5 or more dislikes
    if comment.dislikes >= 5:
        comment.is_hidden = True
    
    db.session.commit()
    
    return jsonify({
        'likes': comment.likes,
        'dislikes': comment.dislikes,
        'hidden': comment.is_hidden
    })

@app.route('/archive')
def archive():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    topics = WeeklyTopic.query.order_by(WeeklyTopic.created_at.desc())\
                             .paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('archive.html', topics=topics)

@app.route('/download_discussion/<int:topic_id>')
def download_discussion(topic_id):
    topic = WeeklyTopic.query.get_or_404(topic_id)
    comments = Comment.query.filter_by(topic_id=topic_id, is_hidden=False)\
                           .order_by(Comment.created_at.asc()).all()
    
    # Create PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    title = topic.title_en if session.get('language') == 'en' else (topic.title_fa or topic.title_en)
    story.append(Paragraph(title, styles['Title']))
    story.append(Spacer(1, 12))
    
    # Content
    content = topic.content_en if session.get('language') == 'en' else (topic.content_fa or topic.content_en)
    story.append(Paragraph(content, styles['Normal']))
    story.append(Spacer(1, 12))
    
    # Comments
    story.append(Paragraph("Comments", styles['Heading1']))
    story.append(Spacer(1, 12))
    
    for comment in comments:
        story.append(Paragraph(f"<b>{comment.author_name}</b> - {comment.created_at.strftime('%Y-%m-%d %H:%M')}", styles['Heading2']))
        story.append(Paragraph(comment.content, styles['Normal']))
        story.append(Spacer(1, 6))
    
    doc.build(story)
    
    buffer.seek(0)
    response = make_response(buffer.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=discussion_{topic_id}.pdf'
    
    return response

@app.route('/info')
def info():
    from models import Founder, TeamMember, FeaturedAuthor

    founder = Founder.query.first()
    featured_author = FeaturedAuthor.query.first()
    team = TeamMember.query.all()

    return render_template('info.html', founder=founder, featured_author=featured_author, team=team)

@app.route('/appeal', methods=['GET', 'POST'])
def appeal():
    form = AppealForm()
    
    if form.validate_on_submit():
        # Get comment ID from form or session
        comment_id = request.form.get('comment_id')
        if not comment_id:
            flash(get_text('invalid_comment'), 'error')
            return redirect(url_for('appeal'))
        
        comment = Comment.query.get(comment_id)
        if not comment or not comment.is_hidden:
            flash(get_text('comment_not_hidden'), 'error')
            return redirect(url_for('appeal'))
        
        appeal = Appeal(
            comment_id=comment_id,
            appellant_name=form.appellant_name.data,
            appellant_email=form.appellant_email.data,
            reason=form.reason.data
        )
        db.session.add(appeal)
        db.session.commit()
        
        flash(get_text('appeal_submitted'), 'success')
        return redirect(url_for('appeal'))
    
    return render_template('appeal.html', form=form)

@app.route('/set_language/<language>')
def set_language(language):
    if language in get_supported_languages():
        session['language'] = language
    return redirect(request.referrer or url_for('home'))

# Admin routes
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(username=form.username.data).first()
        if admin and check_password_hash(admin.password_hash, form.password.data):
            login_user(admin, remember=form.remember_me.data)
            return redirect(url_for('admin_dashboard'))
        flash(get_text('invalid_credentials'), 'error')
    
    return render_template('admin/login.html', form=form)

@app.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/admin')
@login_required
def admin_dashboard():
    # Statistics
    total_topics = WeeklyTopic.query.count()
    total_comments = Comment.query.count()
    hidden_comments = Comment.query.filter_by(is_hidden=True).count()
    pending_appeals = Appeal.query.filter_by(status='pending').count()
    
    recent_comments = Comment.query.order_by(Comment.created_at.desc()).limit(5).all()
    
    # Get current topics and stories for management
    current_topics = WeeklyTopic.query.order_by(WeeklyTopic.created_at.desc()).limit(5).all()
    current_stories = WeeklyStory.query.order_by(WeeklyStory.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html',
                         total_topics=total_topics,
                         total_comments=total_comments,
                         hidden_comments=hidden_comments,
                         pending_appeals=pending_appeals,
                         recent_comments=recent_comments,
                         current_topics=current_topics,
                         current_stories=current_stories)

@app.route('/admin/post_topic', methods=['GET', 'POST'])
@login_required
def admin_post_topic():
    form = WeeklyTopicForm()
    
    if form.validate_on_submit():
        # Deactivate current active topic
        current_active = WeeklyTopic.query.filter_by(is_active=True).first()
        if current_active:
            current_active.is_active = False
        
        topic = WeeklyTopic(
            title_en=form.title_en.data,
            title_fa=form.title_fa.data,
            content_en=form.content_en.data,
            content_fa=form.content_fa.data,
            admin_id=current_user.id
        )
        db.session.add(topic)
        db.session.commit()
        
        # Update Excel with latest data
        try:
            from excel_manager import excel_manager
            excel_manager.export_all_data()
        except Exception as e:
            print(f"Excel export error: {e}")
        
        flash(get_text('topic_posted'), 'success')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('admin/dashboard.html', topic_form=form)

@app.route('/admin/post_story', methods=['GET', 'POST'])
@login_required
def admin_post_story():
    form = WeeklyStoryForm()
    
    if form.validate_on_submit():
        # Deactivate current active story
        current_active = WeeklyStory.query.filter_by(is_active=True).first()
        if current_active:
            current_active.is_active = False
        
        story = WeeklyStory(
            title_en=form.title_en.data,
            title_fa=form.title_fa.data,
            content_en=form.content_en.data,
            content_fa=form.content_fa.data,
            author_en=form.author_en.data,
            author_fa=form.author_fa.data,
            admin_id=current_user.id
        )
        db.session.add(story)
        db.session.commit()
        
        # Update Excel with latest data
        try:
            from excel_manager import excel_manager
            excel_manager.export_all_data()
        except Exception as e:
            print(f"Excel export error: {e}")
        
        flash(get_text('story_posted'), 'success')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('admin/dashboard.html', story_form=form)

from werkzeug.utils import secure_filename

@app.route('/admin/manage-info', methods=['GET', 'POST'])
@login_required
def admin_manage_info():
    from models import Founder, TeamMember, FeaturedAuthor
    from forms import FounderForm, TeamMemberForm, FeaturedAuthorForm

    founder = Founder.query.first()
    featured_author = FeaturedAuthor.query.first()
    team_members = TeamMember.query.all()

    founder_form = FounderForm(obj=founder)
    featured_form = FeaturedAuthorForm(obj=featured_author)
    team_form = TeamMemberForm()

    if founder_form.submit.data and founder_form.validate_on_submit():
        if not founder:
            founder = Founder()
        founder.name = founder_form.name.data
        founder.bio = founder_form.bio.data
        file = founder_form.photo.data
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            founder.photo_filename = filename
        db.session.add(founder)
        db.session.commit()
        flash("Founder info updated", "success")
        return redirect(url_for('admin_manage_info'))

    if featured_form.submit.data and featured_form.validate_on_submit():
        if not featured_author:
            featured_author = FeaturedAuthor()
        featured_author.name = featured_form.name.data
        featured_author.bio = featured_form.bio.data
        file = featured_form.photo.data
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            featured_author.photo_filename = filename
        db.session.add(featured_author)
        db.session.commit()
        flash("Featured Author updated", "success")
        return redirect(url_for('admin_manage_info'))

    if team_form.submit.data and team_form.validate_on_submit():
        member = TeamMember(
            name=team_form.name.data,
            role=team_form.role.data
        )
        file = team_form.photo.data
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            member.photo_filename = filename
        db.session.add(member)
        db.session.commit()
        flash("New team member added", "success")
        return redirect(url_for('admin_manage_info'))

    return render_template('admin/manage_info.html',
                           founder_form=founder_form,
                           featured_form=featured_form,
                           team_form=team_form,
                           team_members=team_members,
                           founder=founder,
                           featured_author=featured_author)

@app.route('/admin/comments')
@login_required
def admin_comments():
    page = request.args.get('page', 1, type=int)
    show_hidden = request.args.get('hidden', 'false') == 'true'
    
    query = Comment.query
    if show_hidden:
        query = query.filter_by(is_hidden=True)
    
    comments = query.order_by(Comment.created_at.desc())\
                   .paginate(page=page, per_page=20, error_out=False)
    
    appeals = Appeal.query.filter_by(status='pending').all()
    
    return render_template('admin/comments.html', 
                         comments=comments, 
                         appeals=appeals,
                         show_hidden=show_hidden)

@app.route('/admin/toggle_comment/<int:comment_id>')
@login_required
def toggle_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    comment.is_hidden = not comment.is_hidden
    db.session.commit()
    
    action = 'hidden' if comment.is_hidden else 'unhidden'
    flash(f'Comment {action} successfully', 'success')
    
    return redirect(url_for('admin_comments'))

@app.route('/admin/delete_comment/<int:comment_id>')
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    
    flash('Comment deleted successfully', 'success')
    return redirect(url_for('admin_comments'))

@app.route('/admin/review_appeal/<int:appeal_id>/<action>')
@login_required
def review_appeal(appeal_id, action):
    if action not in ['approve', 'reject']:
        flash('Invalid action', 'error')
        return redirect(url_for('admin_comments'))
    
    appeal = Appeal.query.get_or_404(appeal_id)
    appeal.status = 'approved' if action == 'approve' else 'rejected'
    appeal.reviewed_at = datetime.utcnow()
    appeal.admin_id = current_user.id
    
    if action == 'approve':
        appeal.comment.is_hidden = False
    
    db.session.commit()
    
    # Update Excel with latest data
    try:
        from excel_manager import excel_manager
        excel_manager.export_all_data()
    except Exception as e:
        print(f"Excel export error: {e}")
    
    flash(f'Appeal {action}d successfully', 'success')
    return redirect(url_for('admin_comments'))

@app.route('/admin/topic/<int:topic_id>/delete', methods=['POST'])
@login_required
def delete_topic(topic_id):
    topic = WeeklyTopic.query.get_or_404(topic_id)
    
    # Delete all associated comments and their votes/appeals first
    comments = Comment.query.filter_by(topic_id=topic.id).all()
    for comment in comments:
        # Delete votes for this comment
        CommentVote.query.filter_by(comment_id=comment.id).delete()
        # Delete appeals for this comment
        Appeal.query.filter_by(comment_id=comment.id).delete()
    
    # Delete all comments for this topic
    Comment.query.filter_by(topic_id=topic.id).delete()
    
    # Delete the topic
    db.session.delete(topic)
    db.session.commit()
    
    flash('Topic and all associated data deleted successfully!', 'success')
    
    # Update Excel with latest data
    try:
        from excel_manager import excel_manager
        excel_manager.export_all_data()
    except Exception as e:
        print(f"Excel export error: {e}")
    
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/story/<int:story_id>/delete', methods=['POST'])
@login_required
def delete_story(story_id):
    story = WeeklyStory.query.get_or_404(story_id)
    
    # Delete the story
    db.session.delete(story)
    db.session.commit()
    
    flash('Story deleted successfully!', 'success')
    
    # Update Excel with latest data
    try:
        from excel_manager import excel_manager
        excel_manager.export_all_data()
    except Exception as e:
        print(f"Excel export error: {e}")
    
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/export-excel')
@login_required
def export_excel():
    """Export all data to Excel files"""
    try:
        from excel_manager import excel_manager
        exported_files = excel_manager.export_all_data()
        flash(f'Excel files exported successfully! {len(exported_files)} files created.', 'success')
    except Exception as e:
        flash(f'Error exporting Excel files: {str(e)}', 'danger')
    
    return redirect(url_for('admin_dashboard'))
@app.route('/init_db')
def init_db():
    from app import db  # Replace 'yourapp' with your app's name if needed
    db.create_all()
    return "Database initialized!"