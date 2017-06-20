from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, RadioField, TextAreaField, HiddenField, PasswordField, IntegerField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import DecimalRangeField


# Form for a new user
class VacationPlannerForm(FlaskForm):
    source = StringField('source',validators=[DataRequired()])
    destination = StringField('destination',validators=[DataRequired()])
    days = IntegerField('days',validators=[DataRequired()])
    weekends = BooleanField('weekends',validators=[DataRequired()], default=True)
    sliderAmount = HiddenField ('sliderAmount')
    costslider = DecimalRangeField('costslider', default=0)
    durationslider = DecimalRangeField('durationslider', default=0)