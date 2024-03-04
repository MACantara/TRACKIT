from flask import Flask, render_template, request, redirect, send_from_directory, make_response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from psycopg2 import connect, Error
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/robot.txt')
def serve_robot_txt():
    return send_from_directory(app.static_folder, request.path[1:])

@app.route("/log-in")
def log_in():
    return render_template('log-in.html')

@app.route("/sign-up")
def sign_up():
    return render_template('sign-up.html')

@app.route("/events-overview")
def events_overview():
    return render_template('events-overview.html')

@app.route("/add-new-event")
def add_new_event():
    return render_template('add-new-event.html')

@app.route("/event-dashboard")
def event_dashboard():
    return render_template("event-dashboard.html")

@app.route("/expenses")
def expenses():
    return render_template("expenses.html")

@app.route("/income")
def income():
    return render_template("income.html")

@app.route("/transaction-history")
def transaction_history():
    return render_template("transaction-history.html")

@app.route("/report")
def report():
    return render_template("report.html")

@app.route("/todo", methods=['POST', 'GET'])
def todo():
    if request.method == 'POST':
        task_content = request.form["task"]
        new_task = Todo(content=task_content)
        
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/todo')
        except:
            return 'There was an issue adding your task'
        
    else: 
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('todo.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/todo')
    except:
        return 'There was an issue deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['task']
        
        try:
            db.session.commit()
            return redirect('/todo')
        except:
            return 'There was an issue updating your task'
    else:
        return render_template('update.html', task=task)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)