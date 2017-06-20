from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, RadioField, TextAreaField, HiddenField, PasswordField, IntegerField
from wtforms.validators import DataRequired


# Form for a new user
class VacationPlannerForm(FlaskForm):
    source = StringField('source',validators=[DataRequired()])
    destination = StringField('destination',validators=[DataRequired()])
    days = IntegerField('days',validators=[DataRequired()])
    weekends = BooleanField('weekends',validators=[DataRequired()], default=True)
