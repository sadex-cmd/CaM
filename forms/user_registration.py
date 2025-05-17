from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, NumberRange
import random

math_test = ['√529', '9 * (-3)⁻²', '(-276)⁻³⁵ / (-276)⁻³⁵']
choice = random.randrange(0, 3)


class RegisterForm(FlaskForm):
    login = StringField('Введите название вашей учетной записи (логин)', validators=[DataRequired()])
    password = PasswordField('Придумайте надежный пароль (минимум 8 символов)', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    age = IntegerField("Введите возраст",
                       validators=[DataRequired(), NumberRange(min=16, max=99, message="Вам должно быть больше 16 лет.")])
    submit_age = IntegerField("Подтвердите, что вам больше 16 лет (решите математическую задачу): "
                              f"{math_test[choice]}", validators=[DataRequired()])
    submit = SubmitField('Создать аккаунт')

