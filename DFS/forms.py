from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, HiddenField, BooleanField, DateField, DecimalField
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

class PromoForm(FlaskForm):
    promo = StringField('Promo')

class PaymentForm(FlaskForm):  # Create Order Form
    # address = SelectField('Address', choices = [])
    payment_method = SelectField('Payment Method', choices = [('Credit Card','Credit Card'),('Cash On Delivery','Cash On Delivery')])
    points = BooleanField('Use points to offset delivery fee?', default = False)
    # promo = StringField('Promo')
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

class RateForm(FlaskForm):
    rating = SelectField('Rating', choices = [('1',1),('2',2),('3',3),('4',4),('5',5)])

class AddCreditCardForm(FlaskForm):
    cc = StringField('CC',validators = [Length(min=16, message = "Card number should have 16 digits"),Length(max=16, message = "Card number should have 16 digits") ])
    bank = SelectField('Bank', choices = [('DBS','DBS'),('POSB','POSB'),('OCBC','OCBC'),('UOB','UOB'),('SCB','SCB'),('Citibank','Citibank')])

class ConfirmForm(FlaskForm):
    hidden = HiddenField()

class CreatePromoForm(FlaskForm): 
    promoId = StringField('Promo ID', validators = [InputRequired(message = 'Input is required')])
    promoCode = StringField('Promo Code', validators = [InputRequired(message = 'Input is required')])
    start_date = DateField('Start Date')
    end_date = DateField('End Date')
    name = StringField("Promo Name", validators = [InputRequired(message = 'Input is required')])

class CreateRestaurantForm(FlaskForm):
    uname = StringField('uname',validators = [InputRequired(message = 'Input is required')])
    password = StringField('password', validators = [InputRequired(message = 'Input is required')])
    rname = StringField('rname',validators = [InputRequired(message = 'Input is required')])
    address = StringField('address',validators = [InputRequired(message = 'Input is required')])
    min_amt = StringField('min_amt',validators = [InputRequired(message = 'Input is required')])

class CreateDeliveryStaffForm(FlaskForm): 
    uname = StringField('uname',validators = [InputRequired(message = 'Input is required')])
    password = StringField('password', validators = [InputRequired(message = 'Input is required')])
    dname = StringField('dname', validators = [InputRequired(message = 'Input is required')])
    flatRate = SelectField('flatRate', choices = [('3', '3'),('4','4')])
    staffType = SelectField('staffType', choices = [('PartTime', 'PartTime'),('FullTime', 'FullTime')])

class CreateFoodItemForm(FlaskForm):
    fname = StringField('Food Name', validators = [InputRequired(message = 'Input is required')])
    price = DecimalField('Price ($)', places=2, rounding=None, validators = [InputRequired(message = 'Input is required')])
    order_limit = StringField('order_limit',validators = [InputRequired(message = 'Input is required')])
    category = SelectField('Category', choices = [('Chinese','Chinese'),('Indian','Indian'), ('Japanese','Japanese'), ('Malay','Malay'), ('Western','Western'), ('Dessert','Dessert')])
    availability = SelectField('Availability', choices = [('True','Available'),('False','Not Available')])
