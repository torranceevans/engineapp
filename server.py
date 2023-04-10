from flask import Flask, render_template, request

from pprint import pformat
import os
import requests


app = Flask(__name__)


@app.route("/")
def login_or_newAccount():
    return render_template("login.html")

@app.route("/create-account")
def create_account():
    return render_template("create-account")

@app.route("/dashboard")
def dashboard_view():
    return render_template("dashboard.html")

@app.route("/create-task")
def create_new_task():
    return render_template("create-task.html")

@app.route("/active-task")
def active_task():
    return render_template("active-task.html")

@app.route("/feedback")
def sharkwords():
    return render_template("feedback")







if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')