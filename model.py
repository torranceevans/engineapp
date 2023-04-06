"""Models for Engine App"""

from flask_sqlalchemy import SQLAlchemy
from datetime import dateTime

db = SQLAlchemy()

class User(db.Model):
    """A user"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fname = db.Column(db.String(15), nullable=False)
    lname = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(30), nullable=False)

class Task(db.Model):
    """A task created by a user"""

    __tablename__ = "tasks"

    task_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer)
    title = db.Column(db.String)
    description = db.Column(db.Text)
    status = db.Column(db.String)
    task_created_at = db.Column(db.DateTime)

class Feedback(db.model):
    """Feedback from users"""

    __tablename__ = "user_feedback"

    feedback_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    task_id = db.Column(db.Integer)
    feedback = db.Column(db.Text)
    feedback_created_at = db.Column(db.DateTime)



def connect_to_db(flask_app, db_uri="postgresql:///#----", echo=False):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")






if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)
