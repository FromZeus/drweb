from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class CreateTaskForm(FlaskForm):
    difficulty = StringField("difficulty", validators=[DataRequired()])


class RetriveTaskForm(FlaskForm):
    id = StringField("id", validators=[DataRequired()])
