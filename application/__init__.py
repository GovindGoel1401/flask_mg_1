from flask import Flask
from flask_pymongo import PyMongo

app= Flask(__name__)
app.config['SECRET_KEY']='d1784e03c2801c5d5bc580027c6cbc5a0650af00'
app.config['MONGO_URI'] = "mongodb+srv://govind1401:Govin1401@cluster0.bfcsavf.mongodb.net/todo_flask?retryWrites=true&w=majority"




# setup mongoDB
mongodb_client=PyMongo(app)
db=mongodb_client.db
from application import routes