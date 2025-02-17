import click
import sys
from models import db, User, Todo
from app import app
from sqlalchemy.exc import IntegrityError


@app.cli.command("init", help="Creates and initializes the database")
def initialize():
  db.drop_all()
  db.create_all()
  bob = User('bob', 'bob@mail.com', 'bobpass')
  bob.todos.append(Todo('wash car', user_id=bob.id))
  db.session.add(bob)
  db.session.commit()
  print(bob)
  print('Database initialized')


@app.cli.command("get-user", help="Retrieves a User")
@click.argument('username', default='bob')
def get_user(username):
  bob = User.query.filter_by(username=username).first()
  if not bob:
    print(f'{username} not found!')
    return
  print(bob)


@app.cli.command('get-users', help="Retrieve all users")
def get_users():
  users = User.query.all()
  print(users)


@app.cli.command("change-email", help="Change user email")
@click.argument('username')
@click.argument('email')
def change_email(username, email):
  bob = User.query.filter_by(username=username).first()
  if not bob:
    print(f'{username} not found!')
    return
  bob.email = email
  db.session.commit()
  print(bob)


@app.cli.command('create-user', help="Create a new user")
@click.argument('username')
@click.argument('email')
@click.argument('password')
def create_user(username, email, password):
  newuser = User(username, email, password)
  try:
    db.session.add(newuser)
    db.session.commit()
  except IntegrityError as e:
    db.session.rollback()

    # Check whether username or email is the issue
    if "UNIQUE constraint failed: user.username" in str(e.orig):
      print("Error: Username already taken!")
    elif "UNIQUE constraint failed: user.email" in str(e.orig):
      print("Error: Email already in use!")
    else:
      print("Error: Username or email already taken!")
  else:
    print(newuser)


@app.cli.command('delete-user', help="Delete a user")
@click.argument('username')
def delete_user(username):
  bob = User.query.filter_by(username=username).first()
  if not bob:
    print(f'{username} not found!')
    return
  db.session.delete(bob)
  db.session.commit()
  print(f'{username} deleted')


@app.cli.command('get-todos', help="Retrieve user todos")
@click.argument('username')
def get_user_todos(username):
  bob = User.query.filter_by(username=username).first()
  if not bob:
    print(f'{username} not found!')
    return
  print(bob.todos)


@app.cli.command('add-todo', help="Add a todo for a user")
@click.argument('username')
@click.argument('text')
def add_task(username, text):
  bob = User.query.filter_by(username=username).first()
  if not bob:
    print(f'{username} not found!')
    return

  new_todo = Todo(text, user_id=bob.id)  # FIXED: Added user_id
  db.session.add(new_todo)
  db.session.commit()
  print(f'Task added: {new_todo.text}')
