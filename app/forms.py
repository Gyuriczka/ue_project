from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class QuestionForm(FlaskForm):
    seat = SelectField(u'In which class would you like to seat?', choices=[(1,1), (2,2), (3,3)])
    sex = SelectField(u'Are you male or female?', choices=[(0, 'Male'), (1,'Female')])
    age = IntegerField(u'How old are you?')
    si = SelectField(u'Do you travel with your siblings / or your partner?', choices=[(0,'Yes'),(1,'No')])
    pa = SelectField(u'Do you travel with your parents?',choices=[(0,'Yes'),(1,'No')])
    title = SelectField(u'Choice your title', choices = [(0,"Mr"), (1,"Miss"), (2,"Mrs"),
                                                         (3,"Master"),(3,"Dr"), (3,"Sir"),(3,"Lady")])
    submit = SubmitField('Submit')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')