import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import click
from flask.cli import with_appcontext

# --- App Configuration ---
# This line makes the paths explicit and foolproof for deployment
app = Flask(__name__, instance_path=os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance'), template_folder='templates')

app.config['SECRET_KEY'] = 'your_secret_key_here'
# This ensures the database is created inside an 'instance' folder
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(app.instance_path, 'tasks.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- Database Model ---
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Task {self.id}>'

# --- Self-Initializing Database ---
# This runs before the first request and creates the DB if it doesn't exist
with app.app_context():
    # Create the instance folder if it doesn't exist
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    db.create_all()

# --- Application Routes ---
@app.route('/')
def index():
    tasks = Task.query.order_by(Task.id).all()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    task_content = request.form['content']
    new_task = Task(content=task_content)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_task(id):
    task_to_delete = Task.query.get_or_404(id)
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_task(id):
    task = Task.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        db.session.commit()
        return redirect(url_for('index'))
    else:
        return render_template('edit.html', task=task)

@app.route('/complete/<int:id>')
def complete_task(id):
    task = Task.query.get_or_404(id)
    task.completed = not task.completed
    db.session.commit()
    return redirect(url_for('index'))

# --- Custom CLI Commands (for local use) ---
@click.command(name='reset-db')
@with_appcontext
def reset_db_command():
    """Wipes and recreates the database."""
    db.drop_all()
    db.create_all()
    click.echo('Database wiped and reset.')

app.cli.add_command(reset_db_command)

if __name__ == "__main__":
    app.run(debug=True)