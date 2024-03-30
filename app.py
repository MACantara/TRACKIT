# Revamp the whole system from scratch
# Add Log in & Register system
# Secure the details from the log in system
# Connect the log in system to the database
# Connect the users to events that user created
# Add ability to update and delete events
# Connect the details of the events based on the event id

from flask import Flask, render_template, request, redirect, send_from_directory, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, current_user, login_required, UserMixin
from datetime import datetime
from pytz import timezone
from psycopg2 import connect, Error
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
from collections import defaultdict
import os
import psycopg2

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

# Add strftime as a custom filter
app.jinja_env.filters['strftime'] = lambda dt: dt.strftime('%m/%d/%Y')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), index=True)
    last_name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(256))
    events = db.relationship('Event', backref='creator', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_active(self):
        # This should return True unless the user has been deactivated.
        return True

    def get_id(self):
        return str(self.user_id)
    
class Event(db.Model):
    event_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text, nullable=False)
    budget = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    expenses = db.relationship('Expense', backref='event', lazy=True)

class Expense(db.Model):
    expense_id = db.Column(db.Integer, primary_key=True)
    expense_name = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    amount = db.Column(db.Float, nullable=False)  # Changed from db.Integer to db.Float
    price = db.Column(db.Float, nullable=False)  # Changed from db.Integer to db.Float
    category = db.Column(db.String(50), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.event_id'), nullable=False)

    @property
    def transaction_type(self):
        return 'Expense'

    def to_dict(self):
        manila = timezone('Asia/Manila')
        date_created_manila = self.date_created.replace(tzinfo=timezone('UTC')).astimezone(manila)
        return {
            'expense_name': self.expense_name,
            'amount': self.amount,
            'date_created': date_created_manila
            # Add any other fields you want to include
        }

    def __repr__(self):
        return '<Expense %r>' % self.expense_id

class Income(db.Model):
    income_id = db.Column(db.Integer, primary_key=True)
    income_name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    event_id = db.Column(db.Integer, db.ForeignKey('event.event_id'), nullable=False)

    @property
    def transaction_type(self):
        return 'Income'

    def to_dict(self):
        manila = timezone('Asia/Manila')
        date_created_manila = self.date_created.replace(tzinfo=timezone('UTC')).astimezone(manila)
        return {
            'income_name': self.income_name,
            'amount': self.amount,
            'date_created': date_created_manila
            # Add any other fields you want to include
        }

    def __repr__(self):
        return f"Income('{self.income_name}', '{self.amount}', '{self.price}', '{self.category}')"

@app.template_filter('localize')
def localize(utc_dt):
    return utc_dt.replace(tzinfo=timezone('UTC')).astimezone(timezone('Asia/Manila'))

@app.template_filter('strftime')
def _jinja2_filter_datetime(date, fmt=None):
    native = date.replace(tzinfo=None)
    format='%b %d, %Y %I:%M %p' if fmt is None else fmt
    return native.strftime(format)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/robot.txt')
def serve_robot_txt():
    return send_from_directory(app.static_folder, request.path[1:])

@app.route("/log-in", methods=['POST', 'GET'])
def log_in():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()
        if user and check_password_hash(user.password_hash, request.form['password']):
            login_user(user)
            return redirect(url_for("events_overview"))
        flash('Invalid username/password')
    return render_template('log-in.html')

@app.route("/sign-up", methods=['POST', 'GET'])
def sign_up():
    if request.method == 'POST':
        new_user = User(
            first_name=request.form['firstname'],
            last_name=request.form['lastname'],
            email=request.form['email'],
            username=request.form['username']
        )
        new_user.set_password(request.form['password'])
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('log_in'))
    return render_template('sign-up.html')

@app.route("/logout")
@login_required
def log_out():
    logout_user()
    return redirect(url_for('index'))

@app.route("/events-overview", methods=['POST', 'GET'])
@login_required
def events_overview():
    events = Event.query.filter_by(user_id=current_user.user_id).all()
    return render_template("events-overview.html", events=events)

# Flask route to render the add event form
@app.route("/add-event-form")
def add_event_form():
    return render_template('add-new-event.html')

@app.route("/add-event", methods=['GET', 'POST'])
@login_required
def add_event():
    if request.method == 'POST':
        event_title = request.form['eventTitle']
        event_date_time = datetime.strptime(request.form['eventDateTime'], '%Y-%m-%dT%H:%M')
        event_description = request.form['eventDescription']
        event_budget = request.form['eventBudget']

        new_event = Event(title=event_title, date=event_date_time, description=event_description, budget=event_budget, user_id=current_user.user_id)
        try:
            db.session.add(new_event)
            db.session.commit()
            return redirect(url_for('event_dashboard', event_id=new_event.event_id))  # Redirect to the new event's dashboard
        except Exception as error:
            return f"Error while adding event to the database: {error}"

    events = Event.query.all()
    return render_template("events-overview.html", events=events)

@app.route('/update-event/<int:event_id>', methods=['GET', 'POST'])
@login_required
def update_event(event_id):
    event = Event.query.get_or_404(event_id)
    if request.method == 'POST':
        event.title = request.form['eventTitle']
        event.date = datetime.strptime(request.form['eventDateTime'], '%Y-%m-%dT%H:%M')
        event.description = request.form['eventDescription']
        event.budget = request.form['eventBudget']
        
        try:
            db.session.commit()
            return redirect(url_for('event_dashboard', event_id=event.event_id))  # Redirect to the updated event's dashboard
        except:
            return 'There was an issue updating your event'
    else:
        return render_template('update-event.html', event=event)

@app.route('/delete-event/<int:event_id>')
@login_required
def delete_event(event_id):
    event_to_delete = Event.query.get_or_404(event_id)
    
    try:
        db.session.delete(event_to_delete)
        db.session.commit()
        return redirect('/events-overview')
    except:
        return 'There was an issue deleting that event'

@app.route("/event-dashboard/<int:event_id>")
@login_required
def event_dashboard(event_id):
    event = Event.query.get_or_404(event_id)
    incomes = Income.query.filter_by(event_id=event.event_id).all()
    expenses = Expense.query.filter_by(event_id=event.event_id).all()
    transactions = incomes + expenses
    transactions.sort(key=lambda x: x.date_created, reverse=True)
    for transaction in transactions:
        if isinstance(transaction, Income):
            transaction.name = transaction.income_name
        else:
            transaction.name = transaction.expense_name
    # Convert incomes and expenses to lists of dictionaries
    incomes = [income.to_dict() for income in incomes]
    expenses = [expense.to_dict() for expense in expenses]
    
    # Calculate daily totals for income and expenses
    daily_incomes = defaultdict(int)
    daily_expenses = defaultdict(int)
    for income in incomes:
        daily_incomes[income['date_created'].date()] += income['amount']
    for expense in expenses:
        daily_expenses[expense['date_created'].date()] += expense['amount']
    
    return render_template("event-dashboard.html", event=event, transactions=transactions, incomes=incomes, expenses=expenses, daily_incomes=daily_incomes, daily_expenses=daily_expenses, budget=event.budget)

@app.route('/expenses/<int:event_id>')
def expenses(event_id):
    event = Event.query.get_or_404(event_id)
    expenses = event.expenses
    return render_template('expenses.html', expenses=expenses, event=event)

@app.route("/add-expense/<int:event_id>", methods=['GET'])
def add_expense(event_id):
    event = Event.query.get_or_404(event_id)
    return render_template("add-expense.html", event=event)

@app.route("/create-expense/<int:event_id>", methods=['POST'])
def create_expense(event_id):
    event = Event.query.get_or_404(event_id)
    if request.method == 'POST':
        expense_name = request.form["expense-name"]
        amount = request.form["amount"]
        price = request.form["price"]
        category = request.form["category"]
        new_expense = Expense(expense_name=expense_name, amount=amount, price=price, category=category, event_id=event.event_id)  # Changed id to event_id

        try:
            db.session.add(new_expense)
            db.session.commit()
            return redirect(url_for('expenses', event_id=event.event_id))  # Changed id to event_id
        except:
            return "There was an issue adding your expense"
    else:
        expenses = event.expenses
        return render_template('expenses.html', expenses=expenses, event=event)

@app.route("/income/<int:event_id>")
def income(event_id):
    event = Event.query.get_or_404(event_id)
    incomes = Income.query.filter_by(event_id=event.event_id).all()
    return render_template("income.html", event=event, incomes=incomes)

@app.route("/add-income/<int:event_id>", methods=['GET', 'POST'])
def add_income(event_id):
    event = Event.query.get_or_404(event_id)
    if request.method == 'POST':
        income_name = request.form["income-name"]
        amount = request.form["amount"]
        price = request.form["price"]
        category = request.form["category"]
        new_income = Income(income_name=income_name, amount=amount, price=price, category=category, event_id=event.event_id)

        try:
            db.session.add(new_income)
            db.session.commit()
            return redirect(url_for('income', event_id=event.event_id))
        except:
            return "There was an issue adding your income"
    else:
        return render_template('add-income.html', event=event)

@app.route("/transaction-history/<int:event_id>")
def transaction_history(event_id):
    event = Event.query.get_or_404(event_id)
    incomes = Income.query.filter_by(event_id=event.event_id).all()
    expenses = Expense.query.filter_by(event_id=event.event_id).all()
    transactions = incomes + expenses
    transactions.sort(key=lambda x: x.date_created, reverse=True)
    for transaction in transactions:
        if isinstance(transaction, Income):
            transaction.name = transaction.income_name
        else:
            transaction.name = transaction.expense_name
    return render_template("transaction-history.html", event=event, transactions=transactions)

@app.route("/report/<int:event_id>")
def report(event_id):
    event = Event.query.get_or_404(event_id)
    return render_template("report.html", event=event)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)