from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, send_from_directory
from datetime import datetime
import os
from dotenv import load_dotenv
from database import is_configured, AccountDB, TransactionDB, BudgetDB
from helpers import format_date

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here-change-in-production')

# Add custom Jinja2 filters
app.jinja_env.filters['format_date'] = format_date

# Check database connection
if not is_configured():
    print("⚠ WARNING: Supabase not configured! Set SUPABASE_URL and SUPABASE_KEY in .env")
    print("⚠ The app will not function without a database connection.")

# Routes
@app.route('/')
def index():
    accounts = AccountDB.get_all()
    total_balance = sum(float(account.get('balance', 0)) for account in accounts)
    recent_transactions = TransactionDB.get_recent(10)
    budgets = BudgetDB.get_all()
    
    # Calculate total income and expenses
    all_transactions = TransactionDB.get_all()
    total_income = sum(float(t.get('amount', 0)) for t in all_transactions if t.get('type') == 'income')
    total_expenses = sum(float(t.get('amount', 0)) for t in all_transactions if t.get('type') == 'expense')
    
    return render_template('index.html', 
                         accounts=accounts, 
                         total_balance=total_balance,
                         recent_transactions=recent_transactions,
                         budgets=budgets,
                         total_income=total_income,
                         total_expenses=total_expenses)

@app.route('/accounts')
def accounts():
    accounts_list = AccountDB.get_all()
    return render_template('accounts.html', accounts=accounts_list)

@app.route('/account/add', methods=['POST'])
def add_account():
    name = request.form.get('name')
    account_type = request.form.get('type')
    balance = float(request.form.get('balance', 0))
    
    AccountDB.create(name, account_type, balance)
    flash('Account added successfully!', 'success')
    return redirect(url_for('accounts'))

@app.route('/account/delete/<int:id>')
def delete_account(id):
    AccountDB.delete(id)
    flash('Account deleted successfully!', 'success')
    return redirect(url_for('accounts'))

@app.route('/transactions')
def transactions():
    transactions_list = TransactionDB.get_all()
    accounts_list = AccountDB.get_all()
    return render_template('transactions.html', transactions=transactions_list, accounts=accounts_list)

@app.route('/transaction/add', methods=['POST'])
def add_transaction():
    account_id = int(request.form.get('account_id'))
    description = request.form.get('description')
    amount = float(request.form.get('amount'))
    category = request.form.get('category')
    trans_type = request.form.get('type')
    
    # Create transaction
    TransactionDB.create(account_id, description, amount, category, trans_type)
    
    # Update account balance
    account = AccountDB.get_by_id(account_id)
    if account:
        current_balance = float(account.get('balance', 0))
        if trans_type == 'income':
            new_balance = current_balance + amount
        else:
            new_balance = current_balance - amount
        AccountDB.update(account_id, balance=new_balance)
        
        # Update budget spent for expenses
        if trans_type == 'expense':
            budget = BudgetDB.get_by_category(category)
            if budget:
                current_spent = float(budget.get('spent', 0))
                BudgetDB.update(budget['id'], spent=current_spent + amount)
    
    flash('Transaction added successfully!', 'success')
    return redirect(url_for('transactions'))

@app.route('/transaction/delete/<int:id>')
def delete_transaction(id):
    transaction = TransactionDB.get_by_id(id)
    
    if transaction:
        # Reverse account balance
        account_id = transaction.get('account_id')
        account = AccountDB.get_by_id(account_id)
        
        if account:
            current_balance = float(account.get('balance', 0))
            amount = float(transaction.get('amount', 0))
            trans_type = transaction.get('type')
            
            if trans_type == 'income':
                new_balance = current_balance - amount
            else:
                new_balance = current_balance + amount
                # Reverse budget spent
                category = transaction.get('category')
                budget = BudgetDB.get_by_category(category)
                if budget:
                    current_spent = float(budget.get('spent', 0))
                    BudgetDB.update(budget['id'], spent=max(0, current_spent - amount))
            
            AccountDB.update(account_id, balance=new_balance)
        
        # Delete transaction
        TransactionDB.delete(id)
        flash('Transaction deleted successfully!', 'success')
    
    return redirect(url_for('transactions'))

@app.route('/budgets')
def budgets():
    budgets_list = BudgetDB.get_all()
    return render_template('budgets.html', budgets=budgets_list)

@app.route('/budget/add', methods=['POST'])
def add_budget():
    category = request.form.get('category')
    limit = float(request.form.get('limit'))
    
    existing_budget = BudgetDB.get_by_category(category)
    if existing_budget:
        BudgetDB.update(existing_budget['id'], limit=limit)
    else:
        BudgetDB.create(category, limit)
    
    flash('Budget updated successfully!', 'success')
    return redirect(url_for('budgets'))

@app.route('/budget/delete/<int:id>')
def delete_budget(id):
    BudgetDB.delete(id)
    flash('Budget deleted successfully!', 'success')
    return redirect(url_for('budgets'))

@app.route('/api/stats')
def api_stats():
    accounts = AccountDB.get_all()
    transactions = TransactionDB.get_all()
    
    stats = {
        'total_balance': sum(float(account.get('balance', 0)) for account in accounts),
        'total_accounts': len(accounts),
        'total_transactions': len(transactions),
        'total_income': sum(float(t.get('amount', 0)) for t in transactions if t.get('type') == 'income'),
        'total_expenses': sum(float(t.get('amount', 0)) for t in transactions if t.get('type') == 'expense')
    }
    
    return jsonify(stats)

@app.route('/service-worker.js')
def service_worker():
    return send_from_directory('static', 'service-worker.js', mimetype='application/javascript')

if __name__ == '__main__':
    app.run(debug=True)
