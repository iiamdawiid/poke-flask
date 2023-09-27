from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class PokemonForm(FlaskForm):
    poke_name = StringField(label='Pokemon Name', validators=[DataRequired()])
    submit = SubmitField()