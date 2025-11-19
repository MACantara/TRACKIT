"""
Seed sample data for TRACKIT application.
Usage: python scripts/seed_data.py [--reset]

This script creates sample Accounts, Transactions, and Budgets in the SQLite database.
If --reset is provided, it will drop and recreate tables to start fresh.
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

from app import app, db, Account, Transaction, Budget


def create_sample_data(reset=False):
    with app.app_context():
        if reset:
            print('Resetting database: dropping and recreating tables...')
            db.drop_all()
            db.create_all()
        else:
            db.create_all()

        # If the DB already has data and we're not resetting, abort (to avoid duplicates)
        if not reset and (Account.query.count() > 0 or Transaction.query.count() > 0 or Budget.query.count() > 0):
            print('Database already contains data. Use --reset to overwrite.')
            return

        # Create accounts
        print('Adding accounts...')
        accounts = [
            Account(name='Main Checking', type='Checking', balance=1200.50),
            Account(name='Savings Account', type='Savings', balance=5500.00),
            Account(name='Rewards Card', type='Credit Card', balance=-250.45),
            Account(name='Wallet', type='Cash', balance=120.00),
        ]
        db.session.add_all(accounts)
        db.session.commit()

        # Add budgets
        print('Adding budgets...')
        budgets = [
            Budget(category='Food', limit=600.00, spent=0.0),
            Budget(category='Transportation', limit=200.00, spent=0.0),
            Budget(category='Entertainment', limit=150.00, spent=0.0),
            Budget(category='Utilities', limit=300.00, spent=0.0),
        ]
        db.session.add_all(budgets)
        db.session.commit()

        # Create transactions
        print('Adding transactions...')
        # Helper to add transaction and update balances/budgets
        def add_transaction(account, description, amount, category, ttype, days_ago=0):
            date = datetime.utcnow() - timedelta(days=days_ago)
            t = Transaction(account_id=account.id, description=description, amount=amount, category=category, type=ttype, date=date)
            # Update account balance
            if ttype == 'income':
                account.balance += amount
            else:
                account.balance -= amount
                # Update budget spent
                budget = Budget.query.filter_by(category=category).first()
                if budget:
                    budget.spent += amount
            db.session.add(t)
            db.session.commit()

        # Add some incomes
        add_transaction(accounts[0], 'Paycheck', 2500.00, 'Salary', 'income', days_ago=10)
        add_transaction(accounts[1], 'Interest', 5.00, 'Investment', 'income', days_ago=20)

        # Add some expenses
        add_transaction(accounts[0], 'Grocery Store', 78.23, 'Food', 'expense', days_ago=4)
        add_transaction(accounts[0], 'Dinner Out', 45.00, 'Food', 'expense', days_ago=5)
        add_transaction(accounts[2], 'Gasoline', 32.50, 'Transportation', 'expense', days_ago=2)
        add_transaction(accounts[2], 'Movie Rental', 12.99, 'Entertainment', 'expense', days_ago=8)
        add_transaction(accounts[0], 'Electric Bill', 95.35, 'Utilities', 'expense', days_ago=15)
        add_transaction(accounts[0], 'Online Shopping', 123.45, 'Shopping', 'expense', days_ago=12)

        print('Refreshing derived balances and budgets...')
        # Commit final balances and budgets
        db.session.commit()

        print('Seed data created successfully.')
        print(f'Total accounts: {Account.query.count()}')
        print(f'Total transactions: {Transaction.query.count()}')
        print(f'Total budgets: {Budget.query.count()}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Seed TRACKIT sample data')
    parser.add_argument('--reset', action='store_true', help='Drop and recreate tables before seeding')
    args = parser.parse_args()

    create_sample_data(reset=args.reset)
