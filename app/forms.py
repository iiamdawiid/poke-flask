from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, validators
from wtforms.validators import DataRequired, EqualTo

class PokemonForm(FlaskForm):
    poke_name = StringField(label='Pokemon Name', validators=[DataRequired()])
    submit = SubmitField()

class SignUpForm(FlaskForm):
    first_name = StringField(label='First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', [DataRequired()])
    email = StringField('Email', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    confirm_password = PasswordField('Confirm Password', [DataRequired(), EqualTo('password')])
    submit = SubmitField()

class LogInForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    submit = SubmitField()

class EditProfileForm(FlaskForm):
    email = StringField(label='New Email', validators=[validators.Optional()])
    confirm_email = StringField(label='Confirm New Email', validators=[validators.Optional()])
    password = PasswordField(label='New Password', validators=[validators.Optional()])
    confirm_password = PasswordField(label='Confirm New Password', validators=[validators.Optional()])
    submit = SubmitField()
    submit = SubmitField()

class CatchPokemonForm(FlaskForm):
    find_pokemon = SubmitField()
    catch = SubmitField()
    # no_catch = SubmitField()

class ReleasePokemonForm(FlaskForm):
    release = SubmitField()