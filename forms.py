from flask_wtf import FlaskForm
from wtforms import DecimalField, SubmitField
from wtforms.validators import DataRequired


class FlipBetForm(FlaskForm):
    betAmt = DecimalField('Bet Amount', validators=[DataRequired()], places=8)

    submit = SubmitField('Click here!')
