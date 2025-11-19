"""
Test database connection for TRACKIT.
Usage: python scripts/test_db.py

This script verifies the database connection and displays information
about the connected database (SQLite or Supabase PostgreSQL).
"""

import os
import sys

# Add parent directory to path
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from database import (
    get_database_uri, 
    is_using_supabase, 
    get_supabase_client,
    SupabaseHelper
)

def test_connection():
    """Test database connection and display info."""
    print("=" * 60)
    print("TRACKIT Database Connection Test")
    print("=" * 60)
    print()
    
    # Check database type
    if is_using_supabase():
        print("✓ Database Type: Supabase PostgreSQL")
        print(f"✓ Connection URI: {get_database_uri()[:50]}...")
        
        # Test Supabase client
        client = get_supabase_client()
        if client:
            print("✓ Supabase client initialized successfully")
            
            # Try to query tables
            try:
                print("\nAttempting to query tables...")
                
                # Test account table
                accounts = SupabaseHelper.select_all('account')
                print(f"  - Accounts: {len(accounts)} records found")
                
                # Test transaction table
                transactions = SupabaseHelper.select_all('transaction')
                print(f"  - Transactions: {len(transactions)} records found")
                
                # Test budget table
                budgets = SupabaseHelper.select_all('budget')
                print(f"  - Budgets: {len(budgets)} records found")
                
                print("\n✓ All tables accessible!")
                
            except Exception as e:
                print(f"\n✗ Error querying tables: {e}")
                print("\nMake sure you've run supabase_schema.sql in Supabase SQL Editor!")
        else:
            print("✗ Supabase client failed to initialize")
    else:
        print("✓ Database Type: SQLite (local development)")
        print(f"✓ Database File: {get_database_uri()}")
        print("\nTo use Supabase PostgreSQL:")
        print("  1. Copy .env.example to .env")
        print("  2. Add your Supabase credentials")
        print("  3. Run supabase_schema.sql in Supabase SQL Editor")
    
    print()
    print("=" * 60)
    print("Connection test complete!")
    print("=" * 60)

if __name__ == '__main__':
    test_connection()
