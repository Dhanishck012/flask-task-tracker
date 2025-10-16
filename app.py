import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import click
from flask.cli import with_appcontext

# --- App Configuration ---
app = Flask(__name__, template_folder='templates')
# The secret key is needed for flash messages
app.config['SECRET_KEY'] = 'your_secret_key_here' # For production, use a real secret key
# Configure the database path
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = f"sqlite:///{os.path.join(project_dir, 'instance', 'tasks.db')}"
app.config['SQLALCHEMY_DATABASE_URI'] = database_file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- Database Model ---
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Task {self.id}>'

# --- Application Routes ---
@app.route('/')
def index():
    tasks = Task.query.order_by(Task.id).all()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
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
    task_to_delete = Task.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect(url_for('index'))
    except:
        return 'There was an issue deleting that task'

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_task(id):
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
    task = Task.query.get_or_404(id)
    task.completed = not task.completed
    try:
        db.session.commit()
        return redirect(url_for('index'))
    except:
        return 'There was an issue updating that task'

# --- Custom CLI Commands ---
@click.command(name='init-db')
@with_appcontext
def init_db_command():
    """Creates the database tables."""
    db.create_all()
    click.echo('Initialized the database.')

@click.command(name='reset-db')
@with_appcontext
def reset_db_command():
    """Wipes and recreates the database."""
    db.drop_all()
    db.create_all()
    click.echo('Database wiped and reset.')

app.cli.add_command(init_db_command)
app.cli.add_command(reset_db_command)

if __name__ == "__main__":
    app.run(debug=True)