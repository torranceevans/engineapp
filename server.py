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


@app.route("/dashboard")     
def dashboard_view():
    """Show details on a particular user."""

    if "user_email" in session:
        user_email = session["user_email"]
        user = crud.get_user_by_email(user_email)

        return render_template("dashboard.html", user=user)

    return redirect("/")

@app.route("/create-task")
def create_task_view():
    """Show create task page."""
    
    return render_template("create-task.html")


                                                        
@app.route("/create-task", methods=["POST"])                         
def create_new_task():
    """Create new task"""

    title = request.form.get("title")
    work_time = request.form.get("work_time")
    rest_time = request.form.get("rest_time")

    new_task = create_task(title, work_time, rest_time)

    db.session.add(new_task)
    db.session.commit()
    flash("Task created!")

    return redirect("/dashboard")




@app.route("/active-task")
def active_task():
    return render_template("active-task.html")

@app.route("/feedback")
def sharkwords():
    return render_template("feedback.html")










if __name__ == '__main__':
    connect_to_db(app)
    app.debug = True
    app.run(host='0.0.0.0')