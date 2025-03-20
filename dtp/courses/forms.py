from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length

class CourseForm(FlaskForm):
    code = StringField('Course Code', validators=[DataRequired(), Length(min=2, max=20)])
    name = StringField('Course Name', validators=[DataRequired(), Length(min=2, max=100)])
    university_id = SelectField('University', coerce=int, validators=[DataRequired()])
    faculty_id = SelectField('Faculty', coerce=int, validators=[DataRequired()])
    department_id = SelectField('Department', coerce=int, validators=[DataRequired()])
    class_id = SelectField('Class Year', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Save')

class CourseFilterForm(FlaskForm):
    university_id = SelectField('University', coerce=int, choices=[])
    faculty_id = SelectField('Faculty', coerce=int, choices=[])
    department_id = SelectField('Department', coerce=int, choices=[])
    class_id = SelectField('Class', coerce=int, choices=[])
    submit = SubmitField('Filter')