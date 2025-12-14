from flask import Flask, Blueprint, redirect, render_template, url_for, request, flash, session as login_session
from app import db
from app.modules import Task

task_bp = Blueprint("task", __name__)

@task_bp.route('/', methods = ["POST", "GET"])
def view_task():
    if 'username' not in login_session:

        return redirect(url_for('auth.login'))
    
    tasks = Task.query.all()
    return render_template('home.html', tasks = tasks)

@task_bp.route('/add', methods = ["POST"])
def add():
    title = request.form.get("title")
    new_task = Task(title = title, status = "Pending")
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('task.view_task'))

@task_bp.route("/clear", methods = ["POST"])
def clear():
    Task.query.delete()
    db.session.commit()
    flash("All task cleared!", "alert")
    return redirect(url_for('task.view_task'))

@task_bp.route("/toggle/<int:task_id>", methods = ["POST"])
def toggle(task_id):

    user = Task.query.get(task_id)
    if user.status == "Pending":
        user.status = "Working"
    elif user.status == "Working":
        user.status = "Done"
    else:
        user.status = "Pending"

    db.session.commit()
    return redirect(url_for('task.view_task'))

