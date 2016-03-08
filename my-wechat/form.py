from flask.ext.wtf import Form
from wtforms import StringField,SubmitField,PasswordField
from wtforms.validators import Email,DataRequired

class LoginForm(Form):
    """docstring for NameForm"""
    name=StringField("what is your name?",validators=[DataRequired()])
    password=PasswordField("please input your password!",validators=[DataRequired()])
    submit=SubmitField(r"login in")

class RegisterForm(Form):
    name=StringField("what is your name?",validators=[DataRequired()])
    password=PasswordField("please input your new password!",validators=[DataRequired()])
    submit=SubmitField(r"register")
