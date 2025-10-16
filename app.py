import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# App and Database Configuration
# Get the absolute path of the directory the script is in
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
# Configuring the database URI to be in an 'instance' folder in the basedir
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance', 'tasks.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Creating the instance folder (if it doesn't exist)
instance_path = os.path.join(basedir, 'instance')
if not os.path.exists(instance_path):
    os.makedirs(instance_path)

db = SQLAlchemy(app)

# Database Model
class Task(db.Model):
    """Represents a single task in the database."""
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Task {self.id}>'

# Application Routes
@app.route('/')
def index():
    """Display all tasks."""
    tasks = Task.query.order_by(Task.id).all()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    """Add a new task."""
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
    """Delete a task."""
    task_to_delete = Task.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect(url_for('index'))
    except:
        return 'There was a problem deleting that task'

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_task(id):
    """Edit an existing task."""
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
    """Mark a task as complete or incomplete."""
    task = Task.query.get_or_404(id)
    task.completed = not task.completed
    try:
        db.session.commit()
        return redirect(url_for('index'))
    except:
        return 'There was an issue updating your task'

## CLI Commands for Database Management
@app.cli.command("init-db")
def init_db_command():
    """Initializes the database with the correct tables."""
    with app.app_context():
        db.create_all()
    print("Initialized the database.")

## Command to wipe and reset the database for a clean start
@app.cli.command("reset-db")
def reset_db_command():
    """Wipes and resets the database."""
    with app.app_context():
        db.drop_all()
        db.create_all()
    print("Database wiped and reset.")

if __name__ == "__main__":
    app.run(debug=True)
