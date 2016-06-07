from flask.ext.wtf import Form
from wtforms import StringField,PasswordField,SubmitField,TextAreaField
from wtforms.validators import ValidationError,Required,Length


class bbsPostForm(Form):
    title=StringField(validators=[Required()])
    text=TextAreaField(validators=[Required()])
    submit=SubmitField()
