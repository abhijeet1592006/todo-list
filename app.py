#MAY-16 2025 10:20 am
#HI MY NAME IS ABHIJEET SINGH AND I AM BUILDNG THIS SMALL APP. HOPE YOU WILL ENJOY IT.


from flask import Flask,render_template,redirect,session,request,url_for #IMPORTING BASIC MODULES
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

    pwd=db.Column(db.String(100),nullable=False)            #here false means this field can not be empty


class Message(db.Model):    #making another table
    id=db.Column(db.Integer,primary_key=True)               
    mid=db.Column(db.Integer,db.ForeignKey('main.id'))
    message=db.Column(db.Text,nullable=True)
    message_priority=db.Column(db.Text,nullable=True)


with app.app_context():
    db.create_all()

@app.route("/",methods=["POST","GET"]) #here i am making a app route to address"/"
def main():
    user=None
    if request.method=="POST":
        user=request.form['user_name']
        p=request.form['pwd']

        data=Data.query.filter(Data.user_name==user).first()
        if data and data.pwd==p:
            session['user']=user
        else:
            return redirect(url_for("reg"))

    if "user" in session:
        return redirect(url_for("your"))
    else:
        return render_template("index.html")


    
@app.route("/register",methods=['POST',"GET"])
def reg():
    if request.method=="POST":
        name=request.form['name']
        user_name=request.form['user_name']
        password=request.form['pwd']
        data1=Data(Name=name,user_name=user_name,pwd=password)
        db.session.add(data1)
        db.session.commit()
        
        return redirect(url_for("main"))
    else:
        return render_template("register.html")
 


    
@app.route("/your-to-do", methods=['POST', "GET"])
def your():
    if 'user' in session:
        cuser = session['user']
        user_data = Data.query.filter_by(user_name=cuser).first()

        todos = Message.query.filter_by(mid=user_data.id).all()

        return render_template("homepage.html", todos=todos, user=cuser)
    else:
        return redirect(url_for("main"))


@app.route("/add-to-do", methods=["POST", "GET"])
def add():
    if 'user' in session:
        uo = session['user']
        h = Data.query.filter(Data.user_name == uo).first()

        if request.method == "POST":
            msg = request.form['addtodo']
            priority = request.form["pri"]  

            new_msg = Message(
                mid=h.id,  
                message=msg,
                message_priority=priority
            )

            db.session.add(new_msg)
            db.session.commit()

            return redirect(url_for("your"))  

        return render_template("addtodo.html")
    else:
        return redirect(url_for("main"))


    
    
    
    
@app.route("/friends-to-do")
def friends_todo():
    if 'user' not in session:
        return redirect(url_for("main"))

    
    all_todos = db.session.query(Message, Data).join(Data, Message.mid == Data.id).all()

    return render_template("friendstodo.html", all_todos=all_todos)



@app.route("/logout")
def logout():
    session.pop('user', None)  
    return redirect(url_for("main"))  

if __name__=="__main__":

   

    app.run(debug=True)