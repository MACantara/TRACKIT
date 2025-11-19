from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trackit.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    balance = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    transactions = db.relationship('Transaction', backref='account', lazy=True, cascade='all, delete-orphan')

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    type = db.Column(db.String(20), nullable=False)  # 'income' or 'expense'

class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False, unique=True)
    limit = db.Column(db.Float, nullable=False)
    spent = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Create tables
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def index():
    accounts = Account.query.all()
    total_balance = sum(account.balance for account in accounts)
    recent_transactions = Transaction.query.order_by(Transaction.date.desc()).limit(10).all()
    budgets = Budget.query.all()
    
    # Calculate total income and expenses
    transactions = Transaction.query.all()
    total_income = sum(t.amount for t in transactions if t.type == 'income')
    total_expenses = sum(t.amount for t in transactions if t.type == 'expense')
    
    return render_template('index.html', 
                         accounts=accounts, 
                         total_balance=total_balance,
                         recent_transactions=recent_transactions,
                         budgets=budgets,
                         total_income=total_income,
                         total_expenses=total_expenses)

@app.route('/accounts')
def accounts():
    accounts = Account.query.all()
    return render_template('accounts.html', accounts=accounts)

@app.route('/account/add', methods=['POST'])
def add_account():
    name = request.form.get('name')
    account_type = request.form.get('type')
    balance = float(request.form.get('balance', 0))
    
    new_account = Account(name=name, type=account_type, balance=balance)
    db.session.add(new_account)
    db.session.commit()
    
    flash('Account added successfully!', 'success')
    return redirect(url_for('accounts'))

@app.route('/account/delete/<int:id>')
def delete_account(id):
    account = Account.query.get_or_404(id)
    db.session.delete(account)
    db.session.commit()
    flash('Account deleted successfully!', 'success')
    return redirect(url_for('accounts'))

@app.route('/transactions')
def transactions():
    transactions = Transaction.query.order_by(Transaction.date.desc()).all()
    accounts = Account.query.all()
    return render_template('transactions.html', transactions=transactions, accounts=accounts)

@app.route('/transaction/add', methods=['POST'])
def add_transaction():
    account_id = int(request.form.get('account_id'))
    description = request.form.get('description')
    amount = float(request.form.get('amount'))
    category = request.form.get('category')
    trans_type = request.form.get('type')
    
    new_transaction = Transaction(
        account_id=account_id,
        description=description,
        amount=amount,
        category=category,
        type=trans_type
    )
    
    # Update account balance
    account = Account.query.get(account_id)
    if trans_type == 'income':
        account.balance += amount
    else:
        account.balance -= amount
        # Update budget spent
        budget = Budget.query.filter_by(category=category).first()
        if budget:
            budget.spent += amount
    
    db.session.add(new_transaction)
    db.session.commit()
    
    flash('Transaction added successfully!', 'success')
    return redirect(url_for('transactions'))

@app.route('/transaction/delete/<int:id>')
def delete_transaction(id):
    transaction = Transaction.query.get_or_404(id)
    
    # Reverse account balance
    account = Account.query.get(transaction.account_id)
    if transaction.type == 'income':
        account.balance -= transaction.amount
    else:
        account.balance += transaction.amount
        # Reverse budget spent
        budget = Budget.query.filter_by(category=transaction.category).first()
        if budget:
            budget.spent -= transaction.amount
    
    db.session.delete(transaction)
    db.session.commit()
    
    flash('Transaction deleted successfully!', 'success')
    return redirect(url_for('transactions'))

@app.route('/budgets')
def budgets():
    budgets = Budget.query.all()
    return render_template('budgets.html', budgets=budgets)

@app.route('/budget/add', methods=['POST'])
def add_budget():
    category = request.form.get('category')
    limit = float(request.form.get('limit'))
    
    existing_budget = Budget.query.filter_by(category=category).first()
    if existing_budget:
        existing_budget.limit = limit
    else:
        new_budget = Budget(category=category, limit=limit)
        db.session.add(new_budget)
    
    db.session.commit()
    flash('Budget updated successfully!', 'success')
    return redirect(url_for('budgets'))

@app.route('/budget/delete/<int:id>')
def delete_budget(id):
    budget = Budget.query.get_or_404(id)
    db.session.delete(budget)
    db.session.commit()
    flash('Budget deleted successfully!', 'success')
    return redirect(url_for('budgets'))

@app.route('/api/stats')
def api_stats():
    accounts = Account.query.all()
    transactions = Transaction.query.all()
    
    stats = {
        'total_balance': sum(account.balance for account in accounts),
        'total_accounts': len(accounts),
        'total_transactions': len(transactions),
        'total_income': sum(t.amount for t in transactions if t.type == 'income'),
        'total_expenses': sum(t.amount for t in transactions if t.type == 'expense')
    }
    
    return jsonify(stats)

if __name__ == '__main__':
    app.run(debug=True)
