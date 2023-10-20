from flask import Flask, render_template, url_for,request,redirect,make_response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import pymysql
import hashlib
app=Flask(__name__)
from urllib.parse import quote_plus

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = (
    "mysql+mysqldb://<user>:<password>@<ip>/<dbname>"
    
)


def hashed(string):
    return hashlib.sha256(string.encode()).hexdigest()


db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.String(64), primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # In a real application, never store plaintext passwords!
    todos = db.relationship('Todo', backref='user', lazy=True)

class Todo(db.Model):
    def current_time():
        return datetime.now() + timedelta(hours=-5)

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=current_time)
    status=db.Column(db.Boolean, default=False)
    userid = db.Column(db.String(64), db.ForeignKey('user.id'), nullable=False)


@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    # if identity match 
    if not request.cookies.get("username"):
        return redirect(url_for("login"))
    
    username=request.cookies.get("username")
    user = User.query.filter_by(username=username).first()
    userid=user.id

    if request.method =='POST':
        try: # POST could be new task or change of checkbox status 

            # Each form in html has several inputs, each has a "name" and a "value". 
            # value = request.form["name"] (request.form looks like a dictionary)

            # You can have hidden input and different values if there are many forms that direct to same route.
            task_content= request.form['content']

            # This calls Todo class, which also returns an ID and the time for this object
            new_task=Todo(content=task_content,userid=userid)

            try:
                db.session.add(new_task)

                # Changes really happen after you "commit"
                db.session.commit()
                return redirect(url_for("home"))
            except:
                return "An issue happen while adding your task"
        except:
            status=(request.form.get("checkbox")=="on")
            id=request.form.get("id")
            task=Todo.query.filter_by(id=id, userid=userid).first()
            # Change the content of the task object
            task.status=status
            db.session.commit()
            return redirect(url_for("home"))


    else:

        # The following code works most of the time. 
        # Tasks are a lists of objects. 
        tasks=Todo.query.filter_by(userid=userid).order_by(Todo.date_created).all()

            # We use "tasks" list in index.html, so we return tasks to html file
        return render_template("index.html",tasks=tasks,id=userid,username=username)
    
@app.route("/delete/<int:id>/<string:userid>")
def delete(id,userid):
    username=request.cookies.get("username")
    if hashed(username)!=userid:
        return "Don't try to delete other user's list!!!!"
    
    
    # Get this object
    task_delete= Todo.query.filter_by(id=id, userid=userid).first()
    try:
        db.session.delete(task_delete)
        db.session.commit()

        # After you delete, go to main page.
        return redirect(url_for("home"))
    except:
        return "Problem while deleting that task"

@app.route("/update/<int:id>/<string:userid>",methods=["GET","POST"])
def update(id,userid):
    username=request.cookies.get("username")
    if hashed(username)!=userid:
        return "Don't try to update other user's list!!!!"
    task=Todo.query.filter_by(id=id, userid=userid).first()
    if request.method=="POST":

        # Change the content of the task object
        task.content=request.form['content']  
        try:
            db.session.commit()
            return redirect(url_for("home"))
        except:
            return "There is an issue updating this task."
    else:

        return render_template("update.html",task=task,hashid=hashed(username))

@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get("password")

        # Check if user exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user!=None:
            return render_template("signup.html",status="Username already exist")

        new_user = User(username=username, password=hashed(password),id=hashed(username))  
        db.session.add(new_user)
        db.session.commit()

        resp = make_response(redirect(url_for("home")))
        resp.set_cookie("username", username)


        return resp
    else:
        return render_template("signup.html",status="")



@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')


        user = User.query.filter_by(username=username).first()

        if not user:
            return render_template("login.html", status="Username does not exist")

        if user.password == hashed(password): 
            resp = make_response(redirect(url_for("home")))
            resp.set_cookie("username", username)
            return resp
        else:
            return render_template("login.html", status="Wrong password")
    else:
        return render_template("login.html", status="")

        

@app.route("/logout")
def logout():
    resp=make_response(redirect(url_for("login")))
    resp.set_cookie("username","",max_age=0)
    return resp


if __name__=="__main__":
    app.run()
    
