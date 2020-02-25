from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import InputRequired, ValidationError, Length


def is_valid_name(form, field):
    if not all(map(lambda char: char.isalpha(), field.data)):
        raise ValidationError('This field should only contain alphabets')


def agrees_terms_and_conditions(form, field):
    if not field.data:
        raise ValidationError('You must agree to the terms and conditions to sign up')


class LoginForm(FlaskForm):
    username = StringField('Username', validators = [InputRequired(message = 'A username is required')])
    password = PasswordField('Password', validators = [InputRequired(message = 'A password is required')])

class RegistrationForm(FlaskForm):
    # firstName = StringField('First Name', validators = [InputRequired(message = 'Input is required')])
    # lastName = StringField('Last Name', validators = [InputRequired(message = "Input is required")])
    username = StringField('Username', validators = [InputRequired(message = 'A username is required')])
    password = PasswordField('Password', validators = [InputRequired(message = 'A password is required')])

class OrderForm(FlaskForm):
    # username = StringField('Username')
    rname = SelectField('rname', choices = [])
    fname = SelectField('fname', choices = [])
