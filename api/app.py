"""
Main application module for the TrackIT web application.

This file sets up the Flask application and configures various parts of it.
"""

import os

from flask import Flask, render_template, request, redirect, \
    send_from_directory, url_for, flash, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, \
    current_user, login_required, UserMixin
from flask_migrate import Migrate
from itsdangerous import URLSafeTimedSerializer
from datetime import datetime
from pytz import timezone
from psycopg2 import connect, Error
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from collections import defaultdict

# Import the reportlab modules for PDF generation
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

# Load environment variables from a .env file
load_dotenv()

app = Flask(__name__)
"""The Flask application instance."""

# Set up the application configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
"""The secret key for the Flask application."""

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
"""The database URL for the Flask application."""

db = SQLAlchemy(app)
"""The SQLAlchemy instance for the Flask application."""

migrate = Migrate(app, db)
"""The Flask-Migrate instance for the Flask application."""

login_manager = LoginManager()
"""The Flask-Login instance for the Flask application."""

login_manager.init_app(app)
"""Initialize the Flask-Login instance for the Flask application."""


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
    events = db.relationship('Event', secondary='user_event', backref=db.backref('users', lazy='dynamic'))

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
    image_filename = db.Column(db.String(200), nullable=True)  # new field for image filename
    expenses = db.relationship('Expense', backref='event', lazy=True)

    def formatted_date(self):
        return datetime.strftime(self.date, "%B %d, %Y")

class UserEvent(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.event_id'), primary_key=True)

class Expense(db.Model):
    expense_id = db.Column(db.Integer, primary_key=True)
    expense_name = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    unit_amount = db.Column(db.Float, nullable=False)  # Changed from db.Integer to db.Float
    price_per_unit = db.Column(db.Float, nullable=False)  # Changed from db.Integer to db.Float
    total_amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.event_id'), nullable=False)

    @property
    def transaction_type(self):
        return 'Expense'

    def to_dict(self):
        manila = timezone('Asia/Manila')
        date_created_manila = self.date_created.replace(tzinfo=timezone('UTC')).astimezone(manila)
        formatted_date = date_created_manila.strftime('%Y-%m-%d %I:%M %p')
        return {
            'expense_name': self.expense_name,
            'total_amount': self.total_amount,
            'date_created': formatted_date
            # Add any other fields you want to include
        }

    def __repr__(self):
        return '<Expense %r>' % self.expense_id

class Income(db.Model):
    income_id = db.Column(db.Integer, primary_key=True)
    income_name = db.Column(db.String(100), nullable=False)
    unit_amount = db.Column(db.Float, nullable=False)
    price_per_unit = db.Column(db.Float, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    event_id = db.Column(db.Integer, db.ForeignKey('event.event_id'), nullable=False)

    @property
    def transaction_type(self):
        return 'Income'

    def to_dict(self):
        manila = timezone('Asia/Manila')
        date_created_manila = self.date_created.replace(tzinfo=timezone('UTC')).astimezone(manila)
        formatted_date = date_created_manila.strftime('%Y-%m-%d %I:%M %p')
        return {
            'income_name': self.income_name,
            'total_amount': self.total_amount,
            'date_created': formatted_date
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
        flash('Invalid username/password', 'danger')
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

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()

        if user:
            token = s.dumps(email, salt='password-reset-salt')
            reset_url = url_for('reset_password', token=token, _external=True)
            msg_body = f'''To reset your password, visit the following link:
{reset_url}

If you did not make this request then simply ignore this email and no changes will be made.
'''
            send_email(email, 'Password Reset Request', msg_body)
            flash('An email has been sent with instructions to reset your password.', 'info')
            return redirect(url_for('log_in'))
        else:
            flash('This email does not exist in our database.', 'warning')
    return render_template('forgot-password.html')

def send_email(to, subject, text):
    msg = MIMEText(text)
    msg['Subject'] = subject
    msg['From'] = os.getenv('GMAIL_EMAIL')
    msg['To'] = to

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(os.getenv('GMAIL_EMAIL'), os.getenv('GMAIL_PASSWORD'))
    s.send_message(msg)
    s.quit()

@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = s.loads(token, salt='password-reset-salt', max_age=3600)
    except:
        flash('The password reset link is invalid or has expired.', 'warning')
        return redirect(url_for('forgot_password'))

    if request.method == 'POST':
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        user.password_hash = generate_password_hash(password)
        db.session.commit()
        user = User.query.filter_by(email=email).first()  # Fetch the user again after the update
        flash('Your password has been updated!', 'success')
        return redirect(url_for('log_in'))

    return render_template('reset-password.html', token=token)

@app.route("/logout")
@login_required
def log_out():
    logout_user()
    return redirect(url_for('index'))

@app.route('/invite/<int:event_id>', methods=['GET', 'POST'])
def invite(event_id):
    if request.method == 'POST':
        email = request.form.get('email')

        # Find the user with the provided email
        user = User.query.filter_by(email=email).first()

        # If no user with that email exists, return an error
        if user is None:
            return 'No user with that email exists', 404

        # Check if the user is already invited
        user_event = UserEvent.query.filter_by(user_id=user.user_id, event_id=event_id).first()
        if user_event is not None:
            return 'User is already invited to this event', 400

        # Create a new UserEvent record
        user_event = UserEvent(user_id=user.user_id, event_id=event_id)
        db.session.add(user_event)
        db.session.commit()

        # Get the event title
        event = Event.query.get(event_id)
        event_title = event.title if event else ''

        # Redirect to the invitation confirmation page with the event title and user email
        return redirect(url_for('invitation_confirmation', event_title=event_title, email=email))

    # Render the invite user form
    return render_template('invite-user.html', event_id=event_id)

@app.route('/invitation-confirmation')
def invitation_confirmation():
    event_title = request.args.get('event_title', '')
    email = request.args.get('email', '')
    return render_template('invitation-confirmation.html', event_title=event_title, email=email)

@app.route("/events-overview", methods=['POST', 'GET'])
@login_required
def events_overview():
    if request.method == 'POST':
        user_id = request.json.get('user_id')
        event_id = request.json.get('event_id')
        user_event = UserEvent.query.filter_by(user_id=user_id, event_id=event_id).first()
        if user_event is None:
            return 'You do not have permission to manage this event', 403
        # Continue with event management...

    events = current_user.events
    return render_template("events-overview.html", events=events)

# Flask route to render the add event form
@app.route("/add-event-form")
def add_event_form():
    return render_template('add-new-event.html')

@app.route("/add-event", methods=['GET', 'POST'])
@login_required
def add_event():
    app.config['UPLOAD_FOLDER'] = '../static/img/'
    if request.method == 'POST':
        event_title = request.form['eventTitle']
        event_date_time = datetime.strptime(request.form['eventDateTime'], '%Y-%m-%dT%H:%M')
        event_description = request.form['eventDescription']
        event_budget = request.form['eventBudget']
        event_image = request.files['eventImage'] if 'eventImage' in request.files else None

        if event_image:
            filename = secure_filename(event_image.filename)
            event_image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            filename = None

        new_event = Event(title=event_title, date=event_date_time, description=event_description, budget=event_budget, image_filename=filename)
        try:
            current_user.events.append(new_event)
            db.session.commit()
            return redirect(url_for('event_dashboard', event_id=new_event.event_id))  # Redirect to the new event's dashboard
        except Exception as error:
            return f"Error while adding event to the database: {error}"

    events = current_user.events
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
        date_created = datetime.strptime(income['date_created'], '%Y-%m-%d %I:%M %p')
        date_created = date_created.date()
        daily_incomes[date_created] += income['total_amount']
    for expense in expenses:
        date_created = datetime.strptime(expense['date_created'], '%Y-%m-%d %I:%M %p')
        date_created = date_created.date()
        daily_expenses[date_created] += expense['total_amount']

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
        unit_amount = request.form["unit_amount"]
        price_per_unit = request.form["price_per_unit"]
        total_amount = request.form["total_amount"]
        category = request.form["category"]
        new_expense = Expense(expense_name=expense_name, unit_amount=unit_amount, price_per_unit=price_per_unit, total_amount=total_amount, category=category, event_id=event.event_id)  # Changed id to event_id

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
        unit_amount = request.form["unit_amount"]
        price_per_unit = request.form["price_per_unit"]
        total_amount = request.form["total_amount"]
        category = request.form["category"]
        new_income = Income(income_name=income_name, unit_amount=unit_amount, price_per_unit=price_per_unit, total_amount=total_amount, category=category, event_id=event.event_id)

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

@app.route('/generate-report/<int:event_id>', methods=['GET'])
def generate_report(event_id):
    event = Event.query.get_or_404(event_id)
    incomes = Income.query.filter_by(event_id=event.event_id).all()
    expenses = Expense.query.filter_by(event_id=event.event_id).all()
    transactions = incomes + expenses
    transactions.sort(key=lambda x: x.date_created, reverse=True)

    data = [["Name", "Date & Time", "Unit Amount", "Price Per Unit", "Total Amount", "Category", "Type"]]
    
    for transaction in transactions:
        if isinstance(transaction, Income):
            transaction.name = transaction.income_name
            transaction.type = "Income"
        else:
            transaction.name = transaction.expense_name
            transaction.type = "Expense"
        
        manila = timezone('Asia/Manila')
        date_created_manila = transaction.date_created.replace(tzinfo=timezone('UTC')).astimezone(manila)
        formatted_date = date_created_manila.strftime('%Y-%m-%d %I:%M %p')

        formatted_unit_amount = '{:,}'.format(transaction.unit_amount)
        formatted_price_per_unit = 'PHP {:,.2f}'.format(transaction.price_per_unit)
        formatted_total_amount = 'PHP {:,.2f}'.format(transaction.total_amount * transaction.price_per_unit)

        data.append([transaction.name, formatted_date, formatted_unit_amount, formatted_price_per_unit, formatted_total_amount, transaction.category, transaction.type])

    filename = f"{event.title}-report.pdf"
    pdf = SimpleDocTemplate(filename, pagesize=letter)

    styles = getSampleStyleSheet()
    header = Paragraph(f"<h1>{event.title} - Generated Report</h1>", styles["Heading1"])

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),

        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),

        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0,0), (-1,-1), 1, colors.black)
    ]))
    elems = []
    elems.append(header)
    elems.append(table)
    pdf.build(elems)

    return send_file(filename, as_attachment=True)

@app.route("/report/<int:event_id>")
def report(event_id):
    event = Event.query.get_or_404(event_id)
    return render_template("report.html", event=event)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)