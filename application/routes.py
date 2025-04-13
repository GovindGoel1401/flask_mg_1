from application import app
from flask import render_template, flash, request,redirect
from datetime import datetime

from application import db 
from .forms import TodoForm

@app.route("/", methods=["GET", "POST"])
def index():
    return  render_template("view_todos.html",title="layout page")

@app.route("/add_todo", methods=["GET", "POST"])
def add_todo():
    if request.method=='POST':
        form = TodoForm(request.form)
        todo_name= form.name.data
        todo_description= form.description.data
        completed= form.completed.data
        
        db.todo_flask.insert_one({
            "name":todo_name,
            "description":todo_description,
            "completed": completed,
            "date_completed":datetime.utcnow()
        })
        flash("Todo Successfully added","Success")
        return redirect("/")
    else:
            form= TodoForm()
    return render_template("add_todo.html",form=form)