-- TRACKIT Database Schema for Supabase PostgreSQL
-- Run this in Supabase SQL Editor to create all tables

-- Drop existing tables if they exist (for fresh setup)
DROP TABLE IF EXISTS transaction CASCADE;
DROP TABLE IF EXISTS budget CASCADE;
DROP TABLE IF EXISTS account CASCADE;

-- Create accounts table
CREATE TABLE account (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(50) NOT NULL,
    balance DOUBLE PRECISION DEFAULT 0.0,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create transactions table
CREATE TABLE transaction (
    id SERIAL PRIMARY KEY,
    account_id INTEGER NOT NULL REFERENCES account(id) ON DELETE CASCADE,
    description VARCHAR(200) NOT NULL,
    amount DOUBLE PRECISION NOT NULL,
    category VARCHAR(50) NOT NULL,
    date TIMESTAMP DEFAULT NOW(),
    type VARCHAR(20) NOT NULL CHECK (type IN ('income', 'expense'))
);

-- Create budgets table
CREATE TABLE budget (
    id SERIAL PRIMARY KEY,
    category VARCHAR(50) NOT NULL UNIQUE,
    "limit" DOUBLE PRECISION NOT NULL,
    spent DOUBLE PRECISION DEFAULT 0.0,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX idx_transaction_account ON transaction(account_id);
CREATE INDEX idx_transaction_date ON transaction(date DESC);
CREATE INDEX idx_transaction_type ON transaction(type);
CREATE INDEX idx_transaction_category ON transaction(category);
CREATE INDEX idx_budget_category ON budget(category);
CREATE INDEX idx_account_type ON account(type);

-- Enable Row Level Security (RLS) - Optional but recommended
ALTER TABLE account ENABLE ROW LEVEL SECURITY;
ALTER TABLE transaction ENABLE ROW LEVEL SECURITY;
ALTER TABLE budget ENABLE ROW LEVEL SECURITY;

-- Create policies for public access (adjust based on your auth requirements)
-- For now, allowing all operations (you can restrict this later with auth)
CREATE POLICY "Allow all operations on account" ON account FOR ALL USING (true);
CREATE POLICY "Allow all operations on transaction" ON transaction FOR ALL USING (true);
CREATE POLICY "Allow all operations on budget" ON budget FOR ALL USING (true);

-- Grant necessary permissions
GRANT ALL ON account TO postgres, anon, authenticated, service_role;
GRANT ALL ON transaction TO postgres, anon, authenticated, service_role;
GRANT ALL ON budget TO postgres, anon, authenticated, service_role;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO postgres, anon, authenticated, service_role;

-- Insert sample data (optional)
INSERT INTO account (name, type, balance) VALUES
    ('Main Checking', 'Checking', 2500.00),
    ('Savings Account', 'Savings', 10000.00),
    ('Credit Card', 'Credit Card', -450.00);

INSERT INTO budget (category, "limit", spent) VALUES
    ('Food', 600.00, 0.00),
    ('Transportation', 200.00, 0.00),
    ('Entertainment', 150.00, 0.00),
    ('Utilities', 300.00, 0.00);

-- Verify tables were created
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
  AND table_type = 'BASE TABLE'
ORDER BY table_name;
