#MAY-16 2025 10:20 am
#HI MY NAME IS ABHIJEET SINGH AND I AM BUILDNG THIS SMALL APP. HOPE YOU WILL ENJOY IT.


from flask import Flask,render_template,redirect,session,request #IMPORTING BASIC MODULES
from flask_sqlalchemy import SQLAlchemy
import os

app=Flask(__name__)         #making our app

app.config["SQLALCHEMY_DATABASE_URI"]='sqlite:///maindatabase.db'#this is for database
app.secret_key="HI ITS ABHIJEET"#this is secret key for our app

db=SQLAlchemy(app)          #for our database

class Data(db.Model):       
    
    __tablename__='main' #making table main with following columns
    id=db.Column(db.Integer,primary_key=True)               
    Name=db.Column(db.String(20),nullable=False)        #here false means this field can not be empty
    user_name=db.Column(db.String(20),nullable=False)   #here false means this field can not be empty

    pwd=db.Column(db.Integer,nullable=False)            #here false means this field can not be empty


class Message(db.Model):    #making another table
    id=db.Column(db.Integer,primary_key=True)               
    mid=db.Column(db.Integer,db.ForeignKey('main.id'))
    message=db.Column(db.Text,nullable=True)
    message_priority=db.Column(db.Text,nullable=True)


with app.app_context():
    db.create_all()

@app.route("/",methods=["POST","GET"]) #here i am making a app route to address"/"
def main():

    if request.method=="POST":


        print(request.form["user_name"])

        print(request.form["pwd"])
        

    return render_template("index.html")


@app.route("/register",methods=['POST',"GET"])
def reg():
    if request.method=="POST":
        print(request.form["name"])

        print(request.form["user_name"])

        print(request.form["pwd"])
        
    return render_template("register.html")
        


if __name__=="__main__":

   

    app.run(debug=True)