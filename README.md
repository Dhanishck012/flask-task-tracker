Zenith Tasks - A Flask-Based Task Tracker

Welcome to Zenith Tasks! This is a simple, clean, and functional web application for managing your daily objectives. I built this project using Python, Flask, and SQLite as part of a screening task for a Software Developer (Fresher) role. It was a fantastic opportunity to build a complete application from scratch, focusing on clean code, a modern user experience, and professional deployment practices.

Crafted with care by Danish Muneer CK.

Live Demo

The application is deployed and live on Render. You can try it out here:

$$Your Live Render App URL Will Go Here$$

Key Features

Fast Task Management: Instantly add new objectives to your list.

Seamless Editing: Modify existing tasks on a dedicated, focused edit page.

Clean Deletion: Remove tasks you no longer need with a confirmation step.

Status Toggling: Easily mark tasks as complete or incomplete with a single click.

Persistent Storage: Your tasks are safely stored in a lightweight SQLite database, so they're always there when you come back.

Fully Responsive: The UI is built with Tailwind CSS to look great and work perfectly on any device—desktop, tablet, or mobile.

Tech Stack

I chose a simple and powerful stack to build this application, focusing on reliability and ease of development.

Backend: Python with the Flask microframework.

Database: SQLite, managed with the Flask-SQLAlchemy ORM for clean and safe queries.

Frontend: HTML templated with Jinja2, and styled with modern, utility-first Tailwind CSS.

Icons: Font Awesome for clean and universally recognized icons.

Deployment: Gunicorn as the WSGI server, hosted on Render's free tier.

Getting Started Locally

Want to run the project on your own machine? Just follow these steps.

1. Prerequisites:

Make sure you have Python 3.8+ and Git installed.

2. Clone the Repository:

git clone [https://github.com/your-username/flask-task-tracker.git](https://github.com/your-username/flask-task-tracker.git)
cd flask-task-tracker

3. Set up a Virtual Environment:

On macOS/Linux:

python3 -m venv venv
source ven/bin/activate

On Windows:

python -m venv venv
.\venv\Scripts\activate

4. Install Dependencies:

pip install -r requirements.txt

5. Initialize the Database:

This command will create a fresh tasks.db file for you.

# In the terminal, run:

python -m flask init-db

Note: If you ever want to start with a clean slate, you can run python -m flask reset-db.

6. Run the App!

python -m flask run

The application will now be running at http://127.0.0.1:5000.

Deployment on Render

This project is configured for a quick and easy deployment on Render.

Push to GitHub: Make sure your final code is in a public GitHub repository.

Create on Render:

Log in to Render and click New > Web Service.

Connect your GitHub account and select your repository.

Set the Configuration:

Runtime: Python 3

Build Command: pip install -r requirements.txt

Start Command: gunicorn app:app

Create the Database on First Deploy:

After the first deploy fails (which is normal), go to the "Environment" tab.

Add a new environment variable with the key FLASK_APP and the value app.py.

Go to the "Shell" tab and run the command flask init-db to create the database on the server.

Go back to your project's dashboard and trigger a new manual deploy. It will now work perfectly.

A Little About My Process

Why Flask? Flask was the required framework for this assignment, and it proved to be an excellent choice. Its minimalist nature was perfect for a project of this scope, allowing me to build exactly what was needed without unnecessary overhead, while still using powerful extensions like SQLAlchemy.

A Note on the UI: My goal was to create an interface that was not just functional but also a pleasure to use. I used Tailwind CSS to build a clean, modern, and responsive design from scratch. I added small touches, like the initial loading animation and the smooth transitions for the task list, to make the application feel more polished and dynamic.

Challenges & Learning: One of the interesting design decisions was how to handle task editing. Instead of trying to edit tasks "inline," which can get complicated on smaller screens, I opted for a separate, dedicated edit page. This makes the main view cleaner and provides a more focused and user-friendly experience when you need to make a change. It was a good lesson in prioritizing clear, simple UX over more complex features.
