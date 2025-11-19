# Supabase PostgreSQL Setup Guide for TRACKIT

## Overview
TRACKIT now supports both **Supabase PostgreSQL** (production) and **SQLite** (local development). The app automatically detects which database to use based on environment variables.

## 🚀 Setup Instructions

### Step 1: Create Supabase Project

1. Go to [Supabase](https://supabase.com) and sign up/login
2. Create a new project
3. Wait for the project to finish setting up (~2 minutes)

### Step 2: Create Database Tables

In your Supabase project dashboard:

1. Go to **SQL Editor**
2. Create a new query
3. Paste and run this SQL:

```sql
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
    type VARCHAR(20) NOT NULL
);

-- Create budgets table
CREATE TABLE budget (
    id SERIAL PRIMARY KEY,
    category VARCHAR(50) NOT NULL UNIQUE,
    limit DOUBLE PRECISION NOT NULL,
    spent DOUBLE PRECISION DEFAULT 0.0,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX idx_transaction_account ON transaction(account_id);
CREATE INDEX idx_transaction_date ON transaction(date);
CREATE INDEX idx_transaction_type ON transaction(type);
CREATE INDEX idx_budget_category ON budget(category);
```

### Step 3: Get Your Credentials

1. Go to **Settings** > **API**
2. Copy these values:
   - **Project URL** (e.g., `https://xxxxx.supabase.co`)
   - **anon public** key (under API Keys)

3. Go to **Settings** > **Database**
4. Copy the **Connection string** > **URI** format
   - It looks like: `postgresql://postgres:[YOUR-PASSWORD]@db.xxxxx.supabase.co:5432/postgres`
   - Replace `[YOUR-PASSWORD]` with your database password

### Step 4: Configure Environment Variables

#### Local Development

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your credentials:
   ```env
   SUPABASE_URL=https://xxxxx.supabase.co
   SUPABASE_KEY=your-anon-key-here
   DATABASE_URL=postgresql://postgres:your-password@db.xxxxx.supabase.co:5432/postgres
   SECRET_KEY=generate-a-random-secret-key
   ```

3. Install python-dotenv to load .env file:
   ```bash
   pip install python-dotenv
   ```

4. Update `app.py` to load environment variables (add at top):
   ```python
   from dotenv import load_dotenv
   load_dotenv()
   ```

#### Vercel Deployment

1. Go to your Vercel project settings
2. Navigate to **Environment Variables**
3. Add these variables:
   - `SUPABASE_URL` = your Supabase URL
   - `SUPABASE_KEY` = your anon key
   - `DATABASE_URL` = your PostgreSQL connection string
   - `SECRET_KEY` = a secure random string

### Step 5: Test Connection

Run the app locally:
```bash
python app.py
```

You should see:
```
✓ Connected to Supabase PostgreSQL
✓ Using Supabase PostgreSQL database
```

If Supabase credentials are not set, it falls back to SQLite:
```
✓ Using SQLite database (local development)
```

## 🔄 Database Migration

### From SQLite to Supabase

If you have existing SQLite data to migrate:

1. Export data from SQLite
2. Use the seed script with Supabase configured:
   ```bash
   python scripts/seed_data.py --reset
   ```

Or manually insert via Supabase dashboard.

## 📊 Table Structure Reference

### `account` table
- `id` (integer, primary key)
- `name` (varchar 100)
- `type` (varchar 50)
- `balance` (double precision)
- `created_at` (timestamp)

### `transaction` table
- `id` (integer, primary key)
- `account_id` (integer, foreign key)
- `description` (varchar 200)
- `amount` (double precision)
- `category` (varchar 50)
- `date` (timestamp)
- `type` (varchar 20) - 'income' or 'expense'

### `budget` table
- `id` (integer, primary key)
- `category` (varchar 50, unique)
- `limit` (double precision)
- `spent` (double precision)
- `created_at` (timestamp)

## 🔐 Security Notes

1. **Never commit `.env` file** - It's in `.gitignore`
2. **Use environment variables** for all secrets
3. **Rotate credentials** periodically
4. **Enable Row Level Security (RLS)** in Supabase for production
5. **Use database password** that's different from your Supabase account password

## 🛠️ Troubleshooting

### "relation does not exist" error
- Tables haven't been created. Run the SQL from Step 2.

### Connection timeout
- Check your DATABASE_URL is correct
- Verify your IP is not blocked (Supabase > Settings > Database > Connection pooling)

### "No module named 'psycopg2'"
- Install dependencies: `pip install -r requirements.txt`

### App uses SQLite instead of Supabase
- Check environment variables are set correctly
- Ensure DATABASE_URL starts with `postgresql://` not `postgres://`

## 🎯 Using Direct Supabase Client

For advanced operations, you can use the Supabase client directly:

```python
from database import get_supabase_client, SupabaseHelper

# Get client
client = get_supabase_client()

# Or use helper methods
accounts = SupabaseHelper.select_all('account')
```

## 📝 Notes

- SQLAlchemy ORM still works the same way
- `database.py` handles the switching automatically
- Both SQLite and PostgreSQL are supported
- No code changes needed in routes/models
