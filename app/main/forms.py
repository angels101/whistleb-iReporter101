
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, BooleanField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError, Email, Required
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed

class PostForm(FlaskForm):
    Type = SelectField('Category', choices=[('Red flag', 'Red flag'), ('Intervention', 'Intervention')], validators=[InputRequired(message="Type required")])
    Title = StringField('Title', validators=[InputRequired(message="Title required")])
    Description = StringField('Description', validators=[InputRequired(message="Description required")])
    submit= SubmitField('Submit')

class AddPostForm(FlaskForm):
    category = SelectField('Category', choices=[('Red flag', 'Red flag'), ('Intervention', 'Intervention')], validators=[InputRequired(message="Category required")])
    title = StringField("Title", validators = [Required()])
    description = TextAreaField("Description", validators = [Required()])
    geolocation = StringField("Geo Location", validators = [Required()])
    submit = SubmitField("Post")


