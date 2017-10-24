from flask_wtf import FlaskForm
from wtforms import IntegerField
from wtforms.validators import DataRequired, NumberRange


class CreateTaskForm(FlaskForm):
    difficulty = IntegerField("difficulty", validators=[NumberRange(0, 1000)])


class RetriveTaskForm(FlaskForm):
    id = IntegerField("id", validators=[DataRequired()])
