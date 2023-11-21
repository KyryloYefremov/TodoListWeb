from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired


class TaskForm(FlaskForm):
    name = StringField("Task Name", validators=[DataRequired()])
    date = DateField("Date", validators=[DataRequired()])
    project = SelectField("Project",  validators=[DataRequired()])
    submit = SubmitField("Submit Task")

    def set_projects(self, existing_projects: list[str]):
        self.project.choices = existing_projects

