from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, EqualTo

class PokemonForm(FlaskForm):
    poke_name = StringField(label='Pokemon Name', validators=[DataRequired()])
    submit = SubmitField()

class SignUpForm(FlaskForm):
    first_name = StringField(label='First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', [DataRequired()])
    email = StringField('Email', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    confirm_password = PasswordField('Confirm Your Password', [DataRequired(), EqualTo('password')])
    submit = SubmitField()

class LogInForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    submit = SubmitField()