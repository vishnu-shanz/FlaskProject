from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Optional

class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired()])
    submit = SubmitField('Save')

class LocationForm(FlaskForm):
    name = StringField('Location Name', validators=[DataRequired()])
    submit = SubmitField('Save')

class ProductMovementForm(FlaskForm):
    product_id = SelectField('Product', coerce=int, validators=[DataRequired()])
    from_location = SelectField('From Location', coerce=int, validators=[Optional()])
    to_location = SelectField('To Location', coerce=int, validators=[Optional()])
    qty = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Save')
