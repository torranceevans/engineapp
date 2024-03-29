"""CRUD operations."""

from model import db, User, Task, Feedback, connect_to_db
import datetime

def create_user(fname, lname, email, password):
    """Create and return a new user."""

    user = User( 
        fname=fname, 
        lname=lname, 
        email=email, 
        password=password)

    return user

def get_users():
    """Return all users."""

    return User.query.all()


def get_user_by_email(email):
    """Return a user by email."""

    return User.query.filter(User.email == email).first()


def create_task(user, title, work_time, rest_time):
    """Create and return a new task."""

    task = Task(
        user=user, # this is using the sqlalchemy relationship (see model.py lines 38 and 19)
        title=title,
        work_time=work_time,
        rest_time=rest_time,
        task_created_at=datetime.datetime.now())

    return task

def create_note(task_id, note):
    """Create and return note."""

    note = Task(
        task_id=task_id,
        note=note)
    
    return note


def get_tasks():
    """Return all tasks."""

    return Task.query.all()


def get_task_by_id(task_id):
    """Return a task by primary key."""

    return Task.query.get(task_id)


def create_feedback(task_id, status, feedback):
    """Create and return new feedback."""

    feedback = Feedback(
        task_id=task_id,
        status=status, 
        feedback=feedback,
        feedback_created_at= datetime.datetime.now())

    return feedback

def delete_task(task_id):
    task = User.query.get(task_id)
    db.session.delete(task)
    db.session.commit()

def delete_user(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()

def edit_task(task_id, **kwargs):
    task = Task.query.get(task_id)
    for key, value in kwargs.items():
        setattr(task, key, value)
    db.session.commit()

def update_user(user_id, **kwargs):
    user = User.query.get(user_id)
    for key, value in kwargs.items():
        setattr(user, key, value)
    db.session.commit()

def update_note(task_id, **kwargs):
    note = Note.query.get(note_id)
    for key, value in kwargs.items():
        setattr(note, key, value)
    db.session.commit()



def update_feedback(feedback_id, new_feedback):
    """ Update feedback given feedback_id and the updated feedback. """
    feedback = Feedback.query.get(feedback_id)
    user_feedback.feedback = new_feedback

if __name__ == "__main__":
    from server import app

    connect_to_db(app)



    



