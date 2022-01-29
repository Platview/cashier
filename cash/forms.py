from flask_wtf import FlaskForm
from wtforms import ValidationError, StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from cash.model import Worker


class RegisterForm(FlaskForm):

    def validate_employee_number(self, employee_number_to_check):
        user = Worker.query.filter_by(employee_number=employee_number_to_check.data).first()
        if user:
            raise ValidationError('EMP already exists! please try a different EMP')

    def validate_email_address(self, email_address_to_check):
        email_address = Worker.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email Address already exists! please try a different email address')

    first_name = StringField(label='First Name', validators=[Length(max=30), DataRequired()])
    last_name = StringField(label='Last Name', validators=[Length(max=30), DataRequired()])
    employee_number = StringField(label='EMP', validators=[Length(5), DataRequired()])
    email_address = StringField(label='Email Address', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')


class LoginForm(FlaskForm):
    employee_number = StringField(label='EMP', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')


# class ItemForm(FlaskForm):
#     item_barcode = StringField(label='Item', validators=[DataRequired()])
#     item_quantity = IntegerField(label='Qty')
#     submit = SubmitField(label='Add')
#
# class EndForm(FlaskForm):
#     submit = SubmitField(label='End Work')