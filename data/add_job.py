from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, BooleanField, IntegerField
from wtforms.validators import DataRequired


class AddJobForm(FlaskForm):
    job = StringField('Название работы', validators=[DataRequired()])
    team_leader = IntegerField('Заказчик')
    work_size = StringField('Размер работы', validators=[DataRequired()])
    collaborators = StringField('Сооснователи', validators=[DataRequired()])
    is_finished = BooleanField('Работа выполнена?')
    submit = SubmitField('Готово!')
