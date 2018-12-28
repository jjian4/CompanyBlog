from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired


#Form for creating and publishing a new post
class NewPostForm(FlaskForm):
    # date/time is handled in Post model definition (models.py)
    title = StringField('Title', validators=[DataRequired()])
    text = TextAreaField('Text', validators=[DataRequired()])

    departments = [("General/Announcements", "General/Announcements"),
                ("Production", "Production"),
                ("Research & Development", "Research & Development"),
                ("Marketing & Sales", "Marketing & Sales"),
                ("Human Resource", "Human Resource"), 
                ("Finance", "Finance"), 
                ("Executive", "Executive")]

    department = SelectField('Department', choices=departments, validators=[DataRequired()])

    submit = SubmitField('Post')
