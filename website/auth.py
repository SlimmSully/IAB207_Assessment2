from flask import Blueprint, flash, render_template, request, url_for, redirect
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash  
from .models import User
from .forms import LoginForm, RegisterForm
from . import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(db.select(User).where(User.name == form.user_name.data))
        if not user or not check_password_hash(user.password_hash, form.password.data):
            flash('Incorrect username or password')
            return render_template('login.html', form=form), 401
        login_user(user)
        nextp = request.args.get('next')
        return redirect(nextp) if nextp and nextp.startswith('/') else redirect(url_for('main.index'))
    return render_template('login.html', form=form)

@auth_bp.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        exists = db.session.scalar(
            db.select(User).where((User.name == form.user_name.data) | (User.email == form.email.data))
        )
        if exists:
            flash('Username or email already in use')
            return render_template('register.html', form=form), 409
        pw_hash = generate_password_hash(form.password.data)
        user = User(name=form.user_name.data, email=form.email.data.lower(), password_hash=pw_hash)
        db.session.add(user)
        db.session.commit()
        flash('Account created. You can log in now.')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    flash('Logged out.')
    return redirect(url_for('main.index'))
