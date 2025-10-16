import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import click
from flask.cli import with_appcontext

# --- App Configuration ---
# This line makes the paths explicit and foolproof for deployment environments like Render.
app = Flask(__name__, instance_path=os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance'), template_folder='templates')

# A secret key is required by Flask to handle sessions and flash messages securely.
app.config['SECRET_KEY'] = 'a-strong-and-random-secret-key' # In a real app, this should be a secure, random value.

# Configure the database URI. This ensures the database file is created
# inside a dedicated 'instance' folder within our project directory.
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(app.instance_path, 'tasks.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the SQLAlchemy extension with our Flask app.
db = SQLAlchemy(app)

# --- Database Model ---
# This class defines the structure of our 'task' table in the database.
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Task {self.id}>'

# --- Self-Initializing Database ---
# This block of code ensures that the database and its tables are created
# automatically when the application starts up. This is a robust pattern
# for platforms like Render.
with app.app_context():
    # Create the instance folder if it doesn't exist to avoid errors.
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass # The folder already exists.
    # Create all tables defined in our models.
    db.create_all()

# --- Application Routes ---
@app.route('/')
def index():
    """The main route, displays all tasks."""
    tasks = Task.query.order_by(Task.id).all()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    """Handles the form submission for adding a new task."""
    task_content = request.form['content']
    new_task = Task(content=task_content)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_task(id):
    """Deletes a task by its ID."""
    task_to_delete = Task.query.get_or_404(id)
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_task(id):
    """Handles both displaying the edit form (GET) and updating the task (POST)."""
    task = Task.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        db.session.commit()
        return redirect(url_for('index'))
    else:
        return render_template('edit.html', task=task)

@app.route('/complete/<int:id>')
def complete_task(id):
    """Toggles the 'completed' status of a task."""
    task = Task.query.get_or_404(id)
    task.completed = not task.completed
    db.session.commit()
    return redirect(url_for('index'))

# --- Custom CLI Command (for local development) ---
@click.command(name='reset-db')
@with_appcontext
def reset_db_command():
    """A command-line helper to wipe and recreate the database during testing."""
    db.drop_all()
    db.create_all()
    click.echo('Database wiped and reset.')

app.cli.add_command(reset_db_command)

# This block allows running the app directly with 'python app.py' for local testing.
if __name__ == "__main__":
    app.run(debug=True)