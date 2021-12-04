from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField , ValidationError
from wtforms.validators import DataRequired

class BlogPostForm(FlaskForm):

    title = StringField('Title',validators=[DataRequired()])
    text = StringField('Description',validators=[DataRequired()])
    submit = SubmitField('Post')