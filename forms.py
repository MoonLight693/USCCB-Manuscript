import re
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

class UploadForm(FlaskForm):
    file = FileField('Upload PDF', validators=[DataRequired()])

class StatusUpdateForm(FlaskForm):
    status = SelectField('Status', choices=[('in review', 'In Review'), ('review complete', 'Review Complete')], validators=[DataRequired()])
    submit = SubmitField('Update')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    display_name = StringField('Display Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match.')])
    submit = SubmitField('Register')

    def validate_password(self, field):
        password = field.data
        # Check length
        if len(password) < 12:
            raise ValidationError('Password must be at least 12 characters long.')

        # Check for uppercase, lowercase, number, and special character
        if not re.search(r'[A-Z]', password):
            raise ValidationError('Password must contain at least one uppercase letter.')
        if not re.search(r'[a-z]', password):
            raise ValidationError('Password must contain at least one lowercase letter.')
        if not re.search(r'\d', password):
            raise ValidationError('Password must contain at least one number.')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError('Password must contain at least one special character (e.g., !@#$%^&*).')
