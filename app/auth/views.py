
from . import auth
from flask import render_template,redirect,url_for,request,flash
from .forms import RegisterForm, LoginForm
from ..models import User
from .. import db
from flask_login import login_user,logout_user,login_required


@auth.route('/register',methods = ["GET","POST"])
def register():
    reg_form = RegisterForm()
    if reg_form.validate_on_submit():
        user=User(username=reg_form.username.data,email=reg_form.email.data,password=reg_form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login'))
        mail_message("Hello, Welcome To Tracy's Blog.", "email/welcome", client.email, subscriber=client)

    return render_template('auth/register.html', form=reg_form)


@auth.route('/login',methods = ["GET","POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user=User.query.filter_by(email=login_form.email.data).first()
        if user is not None and user.verify_password(login_form.password.data):
            login_user(user,login_form.remember.data)
            return redirect(request.args.get('next') or url_for('main.index'))

        flash('Invalid username or Password')

    return render_template('auth/login.html', form=login_form)


@auth.route('/logout')
@login_required
def logout():
    """Logout function"""
    logout_user()
    return redirect(url_for('main.index'))



