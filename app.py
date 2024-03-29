# TODO: Revamp the whole system from scratch
# TODO: Add Log in & Register system
# TODO: Secure the details from the log in system
# TODO: Add a secure forget password mechanism
# TODO: Connect the log in system to the database

from flask import Flask, render_template, request, redirect, send_from_directory, make_response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from psycopg2 import connect, Error
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
import os
import psycopg2

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id
    
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    expense_name = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    amount = db.Column(db.Float, nullable=False)  # Changed from db.Integer to db.Float
    price = db.Column(db.Float, nullable=False)  # Changed from db.Integer to db.Float
    category = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Expense %r>' % self.id
    
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text, nullable=False)
    budget = db.Column(db.Float, nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/robot.txt')
def serve_robot_txt():
    return send_from_directory(app.static_folder, request.path[1:])

@app.route("/log-in", methods=['POST', 'GET'])
def log_in():
    return render_template('log-in.html')

@app.route("/sign-up", methods=['POST', 'GET'])
def sign_up():
    return render_template('sign-up.html')

@app.route("/events-overview", methods=['POST', 'GET'])
def events_overview():
    events = Event.query.all()
    return render_template("events-overview.html", events=events)

# Flask route to render the add event form
@app.route("/add-event-form")
def add_event_form():
    return render_template('add-new-event.html')

# Flask route to handle the form submission and add the event to the database
@app.route("/add-event", methods=['GET', 'POST'])
def add_event():
    if request.method == 'POST':
        event_title = request.form['eventTitle']
        event_date_time = datetime.strptime(request.form['eventDateTime'], '%Y-%m-%dT%H:%M')
        event_description = request.form['eventDescription']
        event_budget = request.form['eventBudget']

        new_event = Event(title=event_title, date=event_date_time, description=event_description, budget=event_budget)
        try:
            db.session.add(new_event)
            db.session.commit()
            redirect("/events-overview")
        except Exception as error:
            return f"Error while adding event to the database: {error}"

    events = Event.query.all()
    return render_template("events-overview.html", events=events)


@app.route("/event-dashboard")
def event_dashboard():
    events = Event.query.all()
    return render_template("event-dashboard.html", events=events)

@app.route('/expenses')
def expenses():
    expenses = Expense.query.all()
    return render_template('expenses.html', expenses=expenses)

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
        task_category = request.form["category"]
        new_task = Todo(content=task_content, category=task_category)
        
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/todo')
        except:
            return 'There was an issue adding your task'
        
    else: 
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('todo.html', tasks=tasks)
    
@app.route("/add-expense", methods=['GET'])
def add_expense():
    return render_template("add-expense.html")

@app.route("/create-expense", methods=['POST'])
def create_expense():
    if request.method == 'POST':
        expense_name = request.form["expense-name"]
        amount = request.form["amount"]
        price = request.form["price"]
        category = request.form["category"]
        new_expense = Expense(expense_name=expense_name, amount=amount, price=price, category=category)

        try:
            db.session.add(new_expense)
            db.session.commit()
            return redirect('/expenses')
        except:
            return "There was an issue adding your expense"
    else:
        expenses = Expense.query.order_by(Expense.date_created).all()
        return render_template('expenses.html', expenses=expenses)

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
        task.category = request.form['category']
        
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