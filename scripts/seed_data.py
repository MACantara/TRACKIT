"""
Seed sample data for TRACKIT application.
Usage: python scripts/seed_data.py [--reset]

This script creates sample Accounts, Transactions, and Budgets in the Supabase database.
If --reset is provided, it will delete all existing data before seeding.
"""

import argparse
from datetime import datetime, timedelta
import random
import os
import sys

# Ensure app directory is on sys.path
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from dotenv import load_dotenv
from database import AccountDB, TransactionDB, BudgetDB, is_configured

# Load environment variables
load_dotenv()


def create_sample_data(reset=False):
    if not is_configured():
        print('ERROR: Supabase not configured!')
        print('Please set SUPABASE_URL and SUPABASE_KEY in your .env file.')
        return

    if reset:
        print('Resetting database: deleting all existing data...')
        # Delete all existing data
        accounts = AccountDB.get_all()
        for account in accounts:
            AccountDB.delete(account['id'])
        budgets = BudgetDB.get_all()
        for budget in budgets:
            BudgetDB.delete(budget['id'])
        print('Existing data deleted.')

    # Create accounts
    print('Adding accounts...')
    account1 = AccountDB.create('Main Checking', 'Checking', 1200.50)
    account2 = AccountDB.create('Savings Account', 'Savings', 5500.00)
    account3 = AccountDB.create('Rewards Card', 'Credit Card', -250.45)
    account4 = AccountDB.create('Wallet', 'Cash', 120.00)

    # Add budgets
    print('Adding budgets...')
    BudgetDB.create('Food', 600.00)
    BudgetDB.create('Transportation', 200.00)
    BudgetDB.create('Entertainment', 150.00)
    BudgetDB.create('Utilities', 300.00)

    # Create transactions
    print('Adding transactions...')
    # Helper to add transaction and update balances/budgets
    def add_transaction(account, description, amount, category, ttype, days_ago=0):
        # Create transaction
        TransactionDB.create(account['id'], description, amount, category, ttype)
        
        # Update account balance
        current_balance = float(account.get('balance', 0))
        if ttype == 'income':
            new_balance = current_balance + amount
        else:
            new_balance = current_balance - amount
            # Update budget spent
            budget = BudgetDB.get_by_category(category)
            if budget:
                current_spent = float(budget.get('spent', 0))
                BudgetDB.update(budget['id'], spent=current_spent + amount)
        
        AccountDB.update(account['id'], balance=new_balance)

    # Add some incomes
    add_transaction(account1, 'Paycheck', 2500.00, 'Salary', 'income', days_ago=10)
    add_transaction(account2, 'Interest', 5.00, 'Investment', 'income', days_ago=20)

    # Add some expenses
    add_transaction(account1, 'Grocery Store', 78.23, 'Food', 'expense', days_ago=4)
    add_transaction(account1, 'Dinner Out', 45.00, 'Food', 'expense', days_ago=5)
    add_transaction(account3, 'Gasoline', 32.50, 'Transportation', 'expense', days_ago=2)
    add_transaction(account3, 'Movie Rental', 12.99, 'Entertainment', 'expense', days_ago=8)
    add_transaction(account1, 'Electric Bill', 95.35, 'Utilities', 'expense', days_ago=15)
    add_transaction(account1, 'Online Shopping', 123.45, 'Shopping', 'expense', days_ago=12)

    print('\nSeed data created successfully.')
    print(f'Total accounts: {len(AccountDB.get_all())}')
    print(f'Total transactions: {len(TransactionDB.get_all())}')
    print(f'Total budgets: {len(BudgetDB.get_all())}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Seed TRACKIT sample data')
    parser.add_argument('--reset', action='store_true', help='Delete existing data before seeding')
    args = parser.parse_args()

    create_sample_data(reset=args.reset)
