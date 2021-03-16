from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, FieldList, HiddenField, TextAreaField, FileField
from wtforms.validators import DataRequired, Email, Length



# class SearchRecipeForm(FlaskForm):
#     """Form for adding/editing messages."""

#     text = TextAreaField('text', validators=[DataRequired()])

class UserSignupForm(FlaskForm):
    """Form for registering users."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])


class AddRecipe(FlaskForm):
    """Form to add new recipe."""

    name = StringField('Recipe Name', validators=[DataRequired()])
    image_url = StringField('Image URL (Optional)')
    cuisine_type = StringField('Cuisine Type')
    ingredients = TextAreaField('List ingredients separated by comma')
    instructions = TextAreaField('Instructions separated by comma')
    user_id = HiddenField()
    