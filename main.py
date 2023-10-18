from flask import Flask, render_template, url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

app=Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'

app.config['SQLALCHEMY_DATABASE_URI'] = (
    'mysql+pymysql://root:_8Ep9>y6xD=gz~9@34.72.207.187/my_to_do_list'
)

db=SQLAlchemy(app)

# Todo is a subclass of db.Model
class Todo(db.Model):
    def current_time():
        return datetime.now() + timedelta(hours=-5)
    
    # These are attributes of the Todo class

    # primary_key is for id. 
    id=db.Column(db.Integer, primary_key=True)
    content=db.Column(db.String(200),nullable=False)
    date_created = db.Column(db.DateTime, default=current_time)

# This is for debugging. Each object have a string name.
    def __repr__(self):
        return '<Task %r>' % self.id


@app.route("/",methods=['POST',"GET"])
def index():
    if request.method =='POST':
        # Each form in html has several inputs, each has a "name" and a "value". 
        # value = request.form["name"] (request.form looks like a dictionary)

        # You can have hidden input and different values if there are many forms that direct to same route.
        task_content= request.form['content']

        # This calls Todo class, which also returns an ID and the time for this object
        new_task=Todo(content=task_content)

        try:
            db.session.add(new_task)

            # Changes really happen after you "commit"
            db.session.commit()
            return redirect("/")
        except:
            return "An issue happen while adding your task"
    else:

        # The following code works most of the time. 
        # Tasks are a lists of objects. 
        tasks=Todo.query.order_by(Todo.date_created).all()

            # We use "tasks" list in index.html, so we return tasks to html file
        return render_template("index.html",tasks=tasks)

@app.route("/delete/<int:id>")
def delete(id):

    # Get this object
    task_delete=Todo.query.get_or_404(id)
    try:
        db.session.delete(task_delete)
        db.session.commit()

        # After you delete, go to main page.
        return redirect('/')
    except:
        return "Problem while deleting that task"

@app.route("/update/<int:id>",methods=["GET","POST"])
def update(id):
    task=Todo.query.get_or_404(id)
    if request.method=="POST":

        # Change the content of the task object
        task.content=request.form['content']  
        try:
            db.session.commit()
            return redirect("/")
        except:
            return "There is an issue updating this task."
    else:
        return render_template("update.html",task=task)
    
if __name__ == '__main__':
    app.run(debug=True)
