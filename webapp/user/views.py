from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user

from webapp.user.forms import LoginForm, RegistrationForm
from webapp.user.models import User
from webapp.db  import db
from webapp.utils import get_redirect_target


blueprint = Blueprint('user', __name__, url_prefix='/users')

@blueprint.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(get_redirect_target)
    title = 'Authorization'
    login_form = LoginForm()
    return render_template('user/login.html', page_title=title, form=login_form)

@blueprint.route('/process-login', methods=['POST'])
def process_login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash('Successfully logged in!')
            return redirect(url_for('news.index'))
    flash('Wrong credentials!')
    return (redirect(url_for('user.login')))

@blueprint.route('/logout')
def logout():
    logout_user()
    flash('Logged out successfully')
    return redirect(get_redirect_target)

@blueprint.route('/register')
def register():
    if current_user.is_authenticated:
        return redirect(url_for('news.index'))
    title = 'Registration'
    registration_form = RegistrationForm()
    return render_template('user/registration.html', page_title=title, form=registration_form)

@blueprint.route('/process-reg', methods=['POST'])
def process_reg():
    form = RegistrationForm()
    if form.validate_on_submit():
        news_user = User(username=form.username.data, email=form.email.data, role='user')
        news_user.set_password(form.password.data)
        db.session.add(news_user)
        db.session.commit()
        flash('Registration successful')
        return redirect(url_for('user.login'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash('Error in field {}: {}'.format(getattr(form, field).label.text, error))
    return redirect(url_for('user.register'))