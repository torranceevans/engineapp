"""CRUD operations."""

from model import db, User, Task, Feedback, connect_to_db

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


def create_task(title, work_time, rest_time):
    """Create and return a new task."""

    task = Task(
        title=title,
        work_time=work_time,
        rest_time=rest_time)

    return task


def get_tasks():
    """Return all tasks."""

    return Task.query.all()


def get_task_by_id(task_id):
    """Return a task by primary key."""

    return Task.query.get(task_id)


def create_feedback(task_id, feedback):
    """Create and return new feedback."""

    feedback = Feedback(task_id=task_id, feedback=feedback)

    return feedback
    

def update_feedback(feedback_id, new_feedback):
    """ Update feedback given feedback_id and the updated feedback. """
    feedback = Feedback.query.get(feedback_id)
    user_feedback.feedback = new_feedback

if __name__ == "__main__":
    from server import app

    connect_to_db(app)



    



