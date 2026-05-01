from flask import Blueprint , render_template,request,flash,redirect,url_for
from werkzeug.security import generate_password_hash , check_password_hash
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

auth=Blueprint('auth',__name__)
@auth.route('/')
def home():
    return render_template("home.html")
@auth.route('/test')
@login_required
def test():
    return render_template("test.html")
@auth.route('/personalities')
def personalities():
    return render_template("personality.html")
@auth.route('/contact')
def contact():
    return render_template("contact.html")
@auth.route('/login')
def login():
    return render_template("login.html")
@auth.route('/register')
def register():
    return render_template("register.html")
@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.home'))
