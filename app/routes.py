from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, QuestionForm
from app.models import User
import numpy as np
from .keras_titanic import titanic_model


@app.route('/')
@app.route('/index')
@login_required
def index():

    return render_template('index.html', title='Home')

@app.route('/survive-simulator', methods=['GET', 'POST'])
@login_required
def survive_simulator():
    form = QuestionForm()
    if form.validate_on_submit():
        seat = float(form.seat.data)
        sex = float(form.sex.data)
        age = float(form.age.data)
        si = float(form.si.data)
        pa = float(form.pa.data)
        title = float(form.title.data)

        user_answer = np.array([seat, sex, age, si, pa, title]).reshape(1, 6)
        result = titanic_model.titanic_simulator(user_answer)
        return render_template('result.html', result=result)
    return render_template('titanic.html', form=form)

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('survive_simulator'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        # next_page = request.args.get('next')
        # if not next_page or url_parse(next_page).netloc != '':
        #     next_page = url_for('index')
        # return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('login'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
