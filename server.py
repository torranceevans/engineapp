from flask import Flask, render_template, request, flash, session, redirect

from model import connect_to_db, db
import crud

from jinja2 import StrictUndefined


app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route("/")
def login_or_newAccount():

    return render_template("homepage.html")


@app.route("/create-user", methods=["POST"])
def register_user():
    """Create a new user."""

    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if user:
        flash("Cannot create an account with that email. Try again.")
    else:
        user = crud.create_user(first_name, last_name, email, password)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.")

    return redirect("/")


@app.route("/login", methods=["POST"])
def process_login():
    """Process user login."""

    email = request.form.get("email")
    password = request.form.get("password")
   
    user = crud.get_user_by_email(email)
   
    if not user or user.password != password:
        flash("The email or password you entered was incorrect.")
        return redirect("/")
    else:
        # Log in user by storing the user's email in session
        session["user_email"] = user.email
        flash(f"Welcome back, {user.fname}!")

    return redirect("/dashboard")

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

# @app.route("/dashboard")
# def create_task_view():
#     """Show dashboard page."""
#     return render_template("dashboard.html")


@app.route("/dashboard", methods=["GET"])     #FIX THIS ROUTE!!!
def dashboard_view():
    """Show details on a particular user."""

    if "user_email" in session:
        user_email = session["user_email"]
        user = crud.get_user_by_email(user_email)

        #Need to display every task input for given user
        #Need to display every feedback page link for every task

        return render_template("dashboard.html", user=user)

    return redirect("/")

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

@app.route("/create-task")
def show_task_form():
    """Show create task page."""
    # TODO: handle user not yet logged in (user_email not in session): probably redirect them to login page
    return render_template("create-task.html")


                                                        
@app.route("/create-task", methods=["POST"])                         
def create_new_task():
    """Create new task"""

    title = request.form.get("title")
    work_time = request.form.get("work_time")
    rest_time = request.form.get("rest_time")

    user_email = session["user_email"] # ---> email=dontbother@all
    user = crud.get_user_by_email(user_email) # --> <User: user_id=4 fname=kat lname=huber-juma email=dontbother@all>
    new_task = crud.create_task(user, title, work_time, rest_time)
    # user is the name of the relationship you set up in model (see model.py line 38 and line 19)
    # sqlalchemy uses the db.relatiosbhionship you set up to represent the one-to-many relationship of user-to-tasks
    # meaning if you have a user object, you can pass that to the sqlalchemy task constructor as Task(user-user_obj) and it will relate the user and task
    # by adding (to the task row (record) in the task table) a foreign key referenceing the user id
    # see lectures data modeling, and maybe sqlalchemy 2

    db.session.add(new_task)
    db.session.commit()
    flash("Task created!")

    return redirect("/dashboard")


    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 


@app.route("/active-task")
def active_task():
    return render_template("active-task.html")

    #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 


@app.route("/feedback")        
def feedback():
    return render_template("feedback")

@app.route("/feedback", methods=["POST"])                         
def create_new_feedback():
    """Create new feedback"""

    status = request.form.get("status")
    feedback = request.form.get("feedback")

    new_feedback = crud.create_feedback(status, feedback)

    db.session.add(new_feedback)
    db.session.commit()
    flash("Feedback logged!")

    return redirect("/dashboard")


@app.route("/feedback-records/<task_id>") 
def display_user_feedback(task_id):
    """Show feedback records on a given task"""

    task = crud.get_task_by_id(task_id)
    # now we have a task object
    # thank to the relationship you set upi in model, 
    # you should be able to get a list of feedback 
    # task.feedback --> [<feedback object>, ... <feedback object>]


    return render_template("feedback-records.html", task=task)









if __name__ == '__main__':
    connect_to_db(app)
    app.debug = True
    app.run(host='0.0.0.0')