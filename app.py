import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import click
from flask.cli import with_appcontext

#  APP CONFIGURATION

# Initialize Flask app and set the template folder
app = Flask(__name__, template_folder='templates')

# Secret key used for securely signing session data (change before production)
app.config['SECRET_KEY'] = 'your_secret_key_here'

# Define database file path (stored inside 'instance' folder)
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = f"sqlite:///{os.path.join(project_dir, 'instance', 'tasks.db')}"

# SQLAlchemy configuration
app.config['SQLALCHEMY_DATABASE_URI'] = database_file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy ORM
db = SQLAlchemy(app)

#  DATABASE MODEL

class Task(db.Model):
    """
    Represents a single Task in the database.
    Each task has:
    - id: unique identifier (integer)
    - content: description of the task (string)
    - completed: boolean flag for task status
    """
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Task {self.id}>'

#  APPLICATION ROUTES

@app.route('/')
def index():
    """
    Home page route:
    - Ensures database/tables are created (only on first run)
    - Retrieves all tasks from the database
    - Renders the index.html template to display tasks
    """
    with app.app_context():
        db.create_all()
    tasks = Task.query.order_by(Task.id).all()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    """
    Route to add a new task:
    - Gets task content from form submission
    - Adds and commits new task to database
    - Redirects back to home page
    """
    task_content = request.form['content']
    new_task = Task(content=task_content)
    try:
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('index'))
    except:
        return 'There was an issue adding your task'

@app.route('/delete/<int:id>')
def delete_task(id):
    """
    Route to delete an existing task:
    - Fetches task by ID
    - Deletes it from database
    """
    task_to_delete = Task.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect(url_for('index'))
    except:
        return 'There was an issue deleting that task'

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_task(id):
    """
    Route to edit an existing task:
    - GET request: Displays edit form
    - POST request: Updates task content in database
    """
    task = Task.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect(url_for('index'))
        except:
            return 'There was an issue updating your task'
    else:
        return render_template('edit.html', task=task)

@app.route('/complete/<int:id>')
def complete_task(id):
    """
    Route to toggle a task's completion status:
    - Flips 'completed' boolean value
    - Commits the update to the database
    """
    task = Task.query.get_or_404(id)
    task.completed = not task.completed
    try:
        db.session.commit()
        return redirect(url_for('index'))
    except:
        return 'There was an issue updating that task'

#  CUSTOM CLI COMMANDS

@click.command(name='init-db')
@with_appcontext
def init_db_command():
    """
    CLI command: Initializes the database.
    Usage: flask init-db
    """
    db.create_all()
    click.echo('✅ Initialized the database.')

@click.command(name='reset-db')
@with_appcontext
def reset_db_command():
    """
    CLI command: Drops all tables and recreates the database.
    Usage: flask reset-db
    """
    db.drop_all()
    db.create_all()
    click.echo('🧹 Database wiped and reset.')

# Register the commands so they can be used via Flask CLI
app.cli.add_command(init_db_command)
app.cli.add_command(reset_db_command)

#  MAIN ENTRY POINT

if __name__ == "__main__":
    # Start the Flask development server
    app.run(debug=True)
