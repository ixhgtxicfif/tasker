from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask import render_template
from datetime import datetime
from flask_migrate import Migrate
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    deadline = db.Column(db.DateTime, nullable=True)
    priority = db.Column(db.Integer, nullable=False, default=1)
    completed = db.Column(db.Boolean, nullable=True)  # Разрешаем использование NULL

if not os.path.exists('tasks.db'):
    with app.app_context():
        db.create_all()

@app.route('/')
def index():
    return 'Привет! Это мой простой менеджер задач.'

@app.route('/tasks')
def tasks():
    tasks = Task.query.all()
    return render_template('tasks.html', tasks=tasks)

@app.route('/task/<int:id>')
def task(id):
    task = Task.query.get_or_404(id)
    return render_template('task.html', task=task)

@app.route('/task/create', methods=['GET', 'POST'])
def create_task():
    if request.method == 'POST':
        description = request.form['description']
        deadline = datetime.strptime(request.form['deadline'], '%Y-%m-%d')
        priority = request.form['priority']
        task = Task(description=description, deadline=deadline, priority=priority)
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('tasks'))
    return render_template('create_task.html')

@app.route('/task/edit/<int:id>', methods=['GET', 'POST'])
def edit_task(id):
    task = Task.query.get_or_404(id)
    if request.method == 'POST':
        task.description = request.form['description']
        task.deadline = datetime.strptime(request.form['deadline'], '%Y-%m-%d')
        task.priority = request.form['priority']
        db.session.commit()
        return redirect(url_for('tasks'))
    return render_template('edit_task.html', task=task)

@app.route('/task/delete/<int:id>', methods=['POST'])
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('tasks'))

@app.route('/task/complete/<int:id>', methods=['POST'])
def complete_task(id):
    task = Task.query.get_or_404(id)
    task.completed = True
    db.session.commit()
    return redirect(url_for('tasks'))

if __name__ == '__main__':
    app.run(debug=True)