from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField


class DelJobForm(FlaskForm):
    is_finished = BooleanField('Действительно удалить?')
    submit = SubmitField('Удалить')
