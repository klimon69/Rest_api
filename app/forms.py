from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Required, Regexp
from app.models import Users

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

class SendMoneyForm(FlaskForm):
    recipient = StringField('Получатель', validators=[DataRequired(), Email()])
    amount = StringField('Сумма', validators=[DataRequired(), Regexp(regex=r'[0-9]')])
    submit = SubmitField('Отправить')


class RegistrationForm(FlaskForm):
    reg_balance = StringField('Начальный баланс', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField(
        'Повторите пароль', validators=[DataRequired(), EqualTo('password')])
    currency_choises = [('1', 'EUR'), ('2', 'USD'), ('3', 'GPB'), ('4', 'RUB'), ('5', 'BTC')]
    currency = SelectField(u'Валюта счета', choices = currency_choises, validators = [Required()])
    submit = SubmitField('Регистрация')

    def validate_username(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Пользователь с таким email уже зарегистрирован в системе')