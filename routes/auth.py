from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required

from extensions import db
from models.user import User
from forms import SignUp, Login
from utils.email import send_email

auth = Blueprint("auth", __name__)


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    
    form = SignUp()
    
    if form.validate_on_submit():
        
        existing_user = User.query.filter_by(
            email=form.email.data.lower()
        ).first()
        
        if existing_user:
            flash("Email already registered", "error")
            return redirect(url_for("auth.signup"))
        
        user = User(
            name=form.name.data,
            email=form.email.data.lower()
        )
        
        user.set_password(form.password.data)
        
        
        db.session.add(user)
        db.session.commit()
        
        
        send_email(
            user.email,
            "Welcome to our website",
            f"<p>Hi {user.name},</p>"
            "<p>Your account has been created successfully.</p>"
            "<p>Thank you for signing up!</p>"
            "<p>Best Regards,<br>Assignment Tracker Team</p>",
        )
             
             
        flash("Account created successfully.", "success")
        
        return redirect(url_for("auth.login"))
    
    return render_template(
        "auth/signup.html",
        form=form
    )
    
    
    
@auth.route("/login", methods=["GET", "POST"])
def login():
    
    form= Login()
    
    if form.validate_on_submit():
        
        user= User.query.filter_by(
            email=form.email.data.lower()
        ).first()
        
        
        if not user or not user.check_password(
            form.password.data
        ):
            
            flash("Invalid email or password.", "error")
            return redirect(url_for("auth.login"))
        
        login_user(user)
        
        if user.is_admin:
            return redirect(url_for("admin.dashboard"))
        
        return redirect(url_for("main.homepage"))
    
    
    return render_template(
        "auth/login.html",
        form=form
    )
    
    
    
@auth.route("/logout")
@login_required
def logout():
    
    logout_user()
    
    return redirect(url_for("auth.login"))






        