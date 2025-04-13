from application import app
from flask import redirect,render_template, flash, request,redirect,url_for

from datetime import datetime

from application import db 
from .forms import TodoForm
from bson import ObjectId

@app.route("/", methods=["GET", "POST"])
def go_todo():
   todos = []
   for todo in db.todo_flask.find().sort("date_created", -1):
         todo["_id"] = str(todo["_id"])
    
         if "date_created" in todo and isinstance(todo["date_created"], datetime):
             todo["date_created"] = todo["date_created"].strftime("%b %d %Y %H:%M:%S")
         else:
             todo["date_created"] = "N/A"  # or any fallback

         todos.append(todo)   
   return  render_template("view_todos.html",title="layout page",todos= todos)

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
            "date_created":datetime.utcnow()
        })
        flash("Todo Successfully added","Success")
        return redirect("/")
    else:
            form= TodoForm()
    return render_template("add_todo.html",form=form)
@app.route("/update_todo/<id>", methods=["POST","GET"])
def update_todo(id):
    if request.method=="POST":
        form = TodoForm(request.form)
        todo_name= form.name.data
        todo_description= form.description.data
        completed= form.completed.data
        
        db.todo_flask.find_one_and_update({"_id": ObjectId(id)},{"$set":{
            "name":todo_name,
            "description":todo_description,
            "completed": completed,
            "date_created":datetime.utcnow()
        }})
        
        flash("Todo successfully updated","success")
        return redirect("/")
    else :
        form =TodoForm()
        
        todo = db.todo_flask.find_one_or_404({"_id":ObjectId(id)})
        form.name.data= todo.get("name",None)
        form.description.data=todo.get("description",None)
        form.completed.data= todo.get("completed",None)
    return render_template("add_todo.html", form=form )    
@app.route("/delete_todo/<id>")
def delete_todo(id):
    db.todo_flask.find_one_and_delete({"_id": ObjectId(id)})
    flash("Todo deleted","success")
    return redirect("/")
    
    