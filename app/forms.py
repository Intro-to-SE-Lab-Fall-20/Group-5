from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField
from flask_wtf.file import FileField

from wtforms.validators import DataRequired, Email, Optional, EqualTo
from wtforms.widgets import Input

#from flask_wysiwyg.wysiwyg import WysiwygField

class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember_me = BooleanField('Remember Me')
	submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	password_2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Register')

		
class RegisterEmailForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	IHostName = StringField('Incoming Mail Server Name', validators=[DataRequired()])
	IPortNum = IntegerField('Incomeing Mail Server Port')
	OHostName = StringField('Outgoing Mail Server Name', validators=[DataRequired()])
	OPortNum = IntegerField('Outgoing Mail Server Port')
	submit = SubmitField('Add')


class ComposeEmail(FlaskForm):
	reciever = StringField('Reciever', validators=[DataRequired(), Email()])
	subject = StringField('Subject', validators=[Optional()])
	message = TextAreaField('Message',validators=[DataRequired()])
	filename = FileField('File',validators=[Optional()])
	submit = SubmitField('Send')
	
