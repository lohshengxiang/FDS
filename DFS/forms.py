from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, HiddenField, BooleanField
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
    firstName = StringField('First Name', validators = [InputRequired(message = 'Input is required')])
    # lastName = StringField('Last Name', validators = [InputRequired(message = "Input is required")])
    username = StringField('Username', validators = [InputRequired(message = 'A username is required')])
    password = PasswordField('Password', validators = [InputRequired(message = 'A password is required')])

class RestaurantForm(FlaskForm):
    rname = SelectField('rname', choices = [])

class OrderForm(FlaskForm):
    # username = StringField('Username')
    # rname = SelectField('rname', choices = [])
    fname = SelectField('fname', choices = [])
    quantity = SelectField('quantity', choices=[])

class PaymentForm(FlaskForm):  # Create Order Form
    # address = SelectField('Address', choices = [])
    payment_method = SelectField('Payment Method', choices = [('Credit Card','Credit Card'),('Cash On Delivery','Cash On Delivery')])
    points = BooleanField('Use points to offset delivery fee?', default = False)
    # address = StringField('Address', validators = [InputRequired(message = 'A username is required')])

class CreditCardForm(FlaskForm):
    cc = SelectField('Credit Card', choices = [])

class AddressForm(FlaskForm):
    address = SelectField('Address', choices = [])


class AddAddressForm(FlaskForm):
    address = StringField('Address', validators = [InputRequired(message = 'An address is required')])

class ChangePasswordForm(FlaskForm):
    oldPassword = PasswordField('Password', validators = [InputRequired(message = 'A password is required')])
    newPassword = PasswordField('Password', validators = [InputRequired(message = 'A password is required')])

class ReviewForm(FlaskForm):
    review = StringField('Review',validators = [Length(min=10, message = "Message must be more than 10 characters")])

class AddCreditCardForm(FlaskForm):
    cc = StringField('CC',validators = [Length(min=16, message = "Card number should have 16 digits"),Length(max=16, message = "Card number should have 16 digits") ])
    bank = SelectField('Bank', choices = [('DBS','DBS'),('POSB','POSB'),('OCBC','OCBC'),('UOB','UOB'),('SCB','SCB'),('Citibank','Citibank')])

class ConfirmForm(FlaskForm):
    hidden = HiddenField()

