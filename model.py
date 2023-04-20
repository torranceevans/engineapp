"""Models for Engine App"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):                   #Need to dropdb - need to find out the name !!!!!!!!!!!!!!!!
    """A user"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fname = db.Column(db.String(15), nullable=False)
    lname = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(30), nullable=False)

    tasks = db.relationship("Task", back_populates="user")

    def __repr__(self):
        return f"<User: user_id={self.user_id} fname={self.fname} lname={self.lname} email={self.email}>"
    


class Task(db.Model):
    """A task created by a user"""

    __tablename__ = "tasks"

    task_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    title = db.Column(db.String, unique=True)
    work_time = db.Column(db.Text, nullable=False) #How to display drop down selection !!!!!!!
    rest_time = db.Column(db.Text, nullable=False) #How to display drop down selection !!!!!!!
    task_created_at = db.Column(db.DateTime)

    user = db.relationship("User", back_populates="tasks")
    feedback = db.relationship("Feedback", back_populates="task")

    def __repr__(self):
        return f"<Task: task_id={self.task_id} title={self.title} user_id={self.user_id} status={self.status}>"


class Feedback(db.Model):
    """Feedback from users"""

    __tablename__ = "user_feedback"

    feedback_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey("tasks.task_id"))
    status = db.Column(db.String, nullable=False) #How to display drop down selection !!!!!!!!!!!!!!!!!!
    feedback = db.Column(db.Text, nullable=False) #How to display drop selection !!!!!!!!!!!!!!!!!!!!!!!!!!!!
    feedback_created_at = db.Column(db.DateTime)

    task = db.relationship("Task", back_populates="feedback")

    def __repr__(self):
        return f"<Feedback: feedback_id={self.feedback_id} feedback={self.feedback}>"



def connect_to_db(flask_app, db_uri="postgresql:///Engine_App", echo=False):
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
    db.drop_all()
    db.create_all()