from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import InputRequired, Optional, URL, NumberRange

class SearchAPIForm(FlaskForm):
    """Form for searching API."""

    query = StringField("Query", validators=[InputRequired()])
    query_type = SelectField("Query Type", choices=[("s", "Cocktail"), ("i", "Ingredient"), ("f", "Letter")])