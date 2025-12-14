from flask import Flask, Blueprint, redirect, render_template, url_for, request, flash, session as login_session
from app.modules import UserInformation
from app import db

auth_bp = Blueprint("auth", __name__)

@auth_bp.route('/login', methods = ["POST", "GET"])
def login():
    
    if request.method == "POST":

        username = request.form.get("username")
        user = UserInformation.query.filter_by(name = username).first()

        if user:

            login_session["username"] = user.name
            flash('Login successfuly!', 'success')
            return redirect(url_for('task.view_task'))
        
        flash("Invalid Credential!", "denger")
        # return render_template("login.html")
    
    return render_template("login.html")


@auth_bp.route('/register', methods = ["POST", "GET"])
def register():
    if request.method == "POST":

        username = request.form.get("username")
        user = UserInformation.query.filter_by(name = username).first()
        if user:
            flash('user alredy exist! choose another username', 'denger')
            return render_template('register.html')
        
        password = request.form.get("password")
        email = request.form.get("email")

        new_user = UserInformation(name = username, password = password, email = email)
        if new_user:
            db.session.add(new_user)
            db.session.commit()

            login_session["username"] = new_user.name

            flash(f'{username}! Register successfuly', 'success')
            return redirect(url_for('task.view_task'))
        
        return "Please enter requred data"
    return render_template("register.html")
        
@auth_bp.route('/logout')
def logout():

    if 'username' not in login_session:

        return redirect(url_for("auth.login"))
    
    login_session.pop('username')
    return redirect(url_for("auth.login"))

