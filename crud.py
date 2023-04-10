"""CRUD operations."""

from model import db, User, Task, Feedback, connect_to_db

def create_user(user_id, fname, lname, email, password):
    """Create and return a new user."""

    user = User(
        user_id=user_id, 
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


def create_task(task_id, user_id, title, description, status, task_created_at):
    """Create and return a new task."""

    task = Task(
        task_id=task_id,                #DOES user_id in task override user_id in user??????
        user_id=user_id,
        title=title,
        description=description,
        status=status,
        task_created_at=task_created_at)

        return task

    



