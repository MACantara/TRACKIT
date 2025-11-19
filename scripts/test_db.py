"""
Test database connection for TRACKIT.
Usage: python scripts/test_db.py

This script verifies the Supabase database connection and displays information
about the connected tables.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add parent directory to path
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from database import get_supabase_client

def test_connection():
    """Test database connection and display info."""
    print("=" * 60)
    print("TRACKIT Database Connection Test")
    print("=" * 60)
    print()
    
    # Check Supabase credentials
    supabase_url = os.environ.get('SUPABASE_URL')
    supabase_key = os.environ.get('SUPABASE_KEY')
    
    if not supabase_url or not supabase_key:
        print("✗ Supabase credentials not found!")
        print("\nPlease set environment variables:")
        print("  1. Copy .env.example to .env")
        print("  2. Add your Supabase credentials")
        print("  3. Run supabase_schema.sql in Supabase SQL Editor")
        return
    
    print(f"✓ Database Type: Supabase PostgreSQL")
    print(f"✓ Supabase URL: {supabase_url}")
    
    # Test Supabase client
    client = get_supabase_client()
    if client:
        print("✓ Supabase client initialized successfully")
        
        # Try to query tables
        try:
            print("\nAttempting to query tables...")
            
            # Test account table
            accounts = client.table('account').select('*').execute()
            print(f"  - Accounts: {len(accounts.data)} records found")
            
            # Test transaction table
            transactions = client.table('transaction').select('*').execute()
            print(f"  - Transactions: {len(transactions.data)} records found")
            
            # Test budget table
            budgets = client.table('budget').select('*').execute()
            print(f"  - Budgets: {len(budgets.data)} records found")
            
            print("\n✓ All tables accessible!")
            
        except Exception as e:
            print(f"\n✗ Error querying tables: {e}")
            print("\nMake sure you've run supabase_schema.sql in Supabase SQL Editor!")
    else:
        print("✗ Supabase client failed to initialize")
    
    print()
    print("=" * 60)
    print("Connection test complete!")
    print("=" * 60)

if __name__ == '__main__':
    test_connection()
