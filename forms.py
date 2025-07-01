from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Optional

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class CommentForm(FlaskForm):
    author_name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    author_email = StringField('Email', validators=[Optional(), Email()])
    content = TextAreaField('Comment', validators=[DataRequired(), Length(min=10, max=700)])
    language = SelectField('Language', choices=[('en', 'English'), ('fa', 'فارسی')], default='en')
    submit = SubmitField('Post Comment')

class WeeklyTopicForm(FlaskForm):
    title_en = StringField('Title (English)', validators=[DataRequired()])
    title_fa = StringField('Title (Persian)', validators=[Optional()])
    content_en = TextAreaField('Content (English)', validators=[DataRequired()])
    content_fa = TextAreaField('Content (Persian)', validators=[Optional()])
    submit = SubmitField('Post Topic')

class WeeklyStoryForm(FlaskForm):
    title_en = StringField('Title (English)', validators=[DataRequired()])
    title_fa = StringField('Title (Persian)', validators=[Optional()])
    content_en = TextAreaField('Content (English)', validators=[DataRequired()])
    content_fa = TextAreaField('Content (Persian)', validators=[Optional()])
    author_en = StringField('Author (English)', validators=[Optional()])
    author_fa = StringField('Author (Persian)', validators=[Optional()])
    submit = SubmitField('Post Story')

class AppealForm(FlaskForm):
    appellant_name = StringField('Your Name', validators=[DataRequired(), Length(min=2, max=100)])
    appellant_email = StringField('Your Email', validators=[DataRequired(), Email()])
    reason = TextAreaField('Reason for Appeal', validators=[DataRequired(), Length(min=20, max=1000)])
    submit = SubmitField('Submit Appeal')
