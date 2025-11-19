"""
Database configuration for TRACKIT using Supabase PostgreSQL.

This module provides a unified interface for database operations using
the official Supabase Python library.
"""

import os
from supabase import create_client, Client
from typing import Optional, List, Dict, Any
from datetime import datetime

# Supabase Configuration
SUPABASE_URL: str = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY: str = os.environ.get("SUPABASE_KEY", "")

# Check if Supabase is configured
USE_SUPABASE = bool(SUPABASE_URL and SUPABASE_KEY)

# Initialize Supabase client
supabase: Optional[Client] = None
if USE_SUPABASE:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("✓ Connected to Supabase PostgreSQL")
    except Exception as e:
        print(f"✗ Failed to connect to Supabase: {e}")
        USE_SUPABASE = False
else:
    print("⚠ Supabase credentials not found. Set SUPABASE_URL and SUPABASE_KEY environment variables.")

def get_supabase() -> Optional[Client]:
    """Get the Supabase client instance."""
    return supabase

def is_configured() -> bool:
    """Check if Supabase is configured and ready."""
    return USE_SUPABASE and supabase is not None

# Account Operations
class AccountDB:
    """Database operations for accounts."""
    
    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        """Get all accounts."""
        if not supabase:
            return []
        try:
            response = supabase.table('account').select('*').order('created_at', desc=True).execute()
            return response.data
        except Exception as e:
            print(f"Error fetching accounts: {e}")
            return []
    
    @staticmethod
    def get_by_id(account_id: int) -> Optional[Dict[str, Any]]:
        """Get account by ID."""
        if not supabase:
            return None
        try:
            response = supabase.table('account').select('*').eq('id', account_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error fetching account {account_id}: {e}")
            return None
    
    @staticmethod
    def create(name: str, account_type: str, balance: float = 0.0) -> Optional[Dict[str, Any]]:
        """Create a new account."""
        if not supabase:
            return None
        try:
            data = {
                'name': name,
                'type': account_type,
                'balance': balance,
                'created_at': datetime.utcnow().isoformat()
            }
            response = supabase.table('account').insert(data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error creating account: {e}")
            return None
    
    @staticmethod
    def update(account_id: int, **kwargs) -> Optional[Dict[str, Any]]:
        """Update an account."""
        if not supabase:
            return None
        try:
            response = supabase.table('account').update(kwargs).eq('id', account_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error updating account {account_id}: {e}")
            return None
    
    @staticmethod
    def delete(account_id: int) -> bool:
        """Delete an account."""
        if not supabase:
            return False
        try:
            supabase.table('account').delete().eq('id', account_id).execute()
            return True
        except Exception as e:
            print(f"Error deleting account {account_id}: {e}")
            return False

# Transaction Operations
class TransactionDB:
    """Database operations for transactions."""
    
    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        """Get all transactions with account info."""
        if not supabase:
            return []
        try:
            response = supabase.table('transaction').select('*, account(*)').order('date', desc=True).execute()
            return response.data
        except Exception as e:
            print(f"Error fetching transactions: {e}")
            return []
    
    @staticmethod
    def get_recent(limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent transactions."""
        if not supabase:
            return []
        try:
            response = supabase.table('transaction').select('*, account(*)').order('date', desc=True).limit(limit).execute()
            return response.data
        except Exception as e:
            print(f"Error fetching recent transactions: {e}")
            return []
    
    @staticmethod
    def get_by_id(transaction_id: int) -> Optional[Dict[str, Any]]:
        """Get transaction by ID."""
        if not supabase:
            return None
        try:
            response = supabase.table('transaction').select('*, account(*)').eq('id', transaction_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error fetching transaction {transaction_id}: {e}")
            return None
    
    @staticmethod
    def create(account_id: int, description: str, amount: float, category: str, trans_type: str) -> Optional[Dict[str, Any]]:
        """Create a new transaction."""
        if not supabase:
            return None
        try:
            data = {
                'account_id': account_id,
                'description': description,
                'amount': amount,
                'category': category,
                'type': trans_type,
                'date': datetime.utcnow().isoformat()
            }
            response = supabase.table('transaction').insert(data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error creating transaction: {e}")
            return None
    
    @staticmethod
    def delete(transaction_id: int) -> bool:
        """Delete a transaction."""
        if not supabase:
            return False
        try:
            supabase.table('transaction').delete().eq('id', transaction_id).execute()
            return True
        except Exception as e:
            print(f"Error deleting transaction {transaction_id}: {e}")
            return False

# Budget Operations
class BudgetDB:
    """Database operations for budgets."""
    
    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        """Get all budgets."""
        if not supabase:
            return []
        try:
            response = supabase.table('budget').select('*').order('category').execute()
            return response.data
        except Exception as e:
            print(f"Error fetching budgets: {e}")
            return []
    
    @staticmethod
    def get_by_category(category: str) -> Optional[Dict[str, Any]]:
        """Get budget by category."""
        if not supabase:
            return None
        try:
            response = supabase.table('budget').select('*').eq('category', category).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error fetching budget for {category}: {e}")
            return None
    
    @staticmethod
    def create(category: str, limit: float) -> Optional[Dict[str, Any]]:
        """Create a new budget."""
        if not supabase:
            return None
        try:
            data = {
                'category': category,
                'limit': limit,
                'spent': 0.0,
                'created_at': datetime.utcnow().isoformat()
            }
            response = supabase.table('budget').insert(data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error creating budget: {e}")
            return None
    
    @staticmethod
    def update(budget_id: int, **kwargs) -> Optional[Dict[str, Any]]:
        """Update a budget."""
        if not supabase:
            return None
        try:
            response = supabase.table('budget').update(kwargs).eq('id', budget_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error updating budget {budget_id}: {e}")
            return None
    
    @staticmethod
    def delete(budget_id: int) -> bool:
        """Delete a budget."""
        if not supabase:
            return False
        try:
            supabase.table('budget').delete().eq('id', budget_id).execute()
            return True
        except Exception as e:
            print(f"Error deleting budget {budget_id}: {e}")
            return False

# Export main components
__all__ = [
    'get_supabase',
    'is_configured',
    'AccountDB',
    'TransactionDB',
    'BudgetDB',
    'supabase'
]
