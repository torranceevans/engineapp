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
    notes = db.relationship("Note", back_populates="task")

    def __repr__(self):
        return f"<Task: task_id={self.task_id} title={self.title} user_id={self.user_id}>"


class Note(db.Model):
    """A note created in a given task by user"""

    __tablename__ = "notes"

    note_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey("tasks.task_id"))
    note = db.Column(db.Text)
    note_created_at = db.Column(db.DateTime)

    task = db.relationship("Task", back_populates="notes")

    def __repr__(self):
        return f"<Note: note_id={self.note_id} task_id {self.title} note={self.note} note_created_at={self.note_created_at}>"
        


class Feedback(db.Model):
    """Feedback from users"""

    __tablename__ = "user_feedback"

    feedback_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey("tasks.task_id"))
    status = db.Column(db.String, nullable=False) 
    feedback = db.Column(db.Text, nullable=False) 
    feedback_created_at = db.Column(db.DateTime)

    task = db.relationship("Task", back_populates="feedback")

    def __repr__(self):
        return f"<Feedback: feedback_id={self.feedback_id} task_id={self.task_id} status={self.status} feedback={self.feedback} feedback_created_at={self.feedback_created_at}>"



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