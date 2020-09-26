from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Optional

class ComposeEmail(FlaskForm):
    reciever = StringField('Reciever', validators=[DataRequired(), Email()])
    subject = StringField('Subject', validators=[Optional()])
    message = TextAreaField('Message',validators=[DataRequired()])
    submit = SubmitField('Send')

