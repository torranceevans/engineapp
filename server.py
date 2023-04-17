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


@app.route("/users", methods=["POST"])
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
        flash(f"Welcome back, {user.fname}!") #IS THIS PULLING FROM THE TABLE?

    return redirect("/dashboard/<user_id>")


@app.route("/dashboard/<user_id>")
def dashboard_view(user_id):
    """Show details on a particular user."""

    user = crud.get_user_by_id(user_id)
    print(f"\n\n********************\n{user}\nuser.email={user.email}\n")

    return render_template("dashboard.html", user=user)


@app.route("/create-task")
def create_new_task():
    return render_template("create-task.html")

@app.route("/active-task")
def active_task():
    return render_template("active-task.html")

@app.route("/feedback")
def sharkwords():
    return render_template("feedback.html")










if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')