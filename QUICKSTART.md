# TRACKIT - Quick Start with Supabase

## 🚀 5-Minute Setup

### 1. Create Supabase Project
1. Go to [supabase.com](https://supabase.com) and create account
2. Click "New Project"
3. Choose a name and password
4. Wait ~2 minutes for setup

### 2. Create Database Tables
1. In Supabase dashboard, go to **SQL Editor**
2. Click "New Query"
3. Copy and paste from `supabase_schema.sql`
4. Click "Run"

### 3. Get Your Credentials
1. Go to **Settings** → **API**
2. Copy:
   - Project URL (e.g., `https://xxxxx.supabase.co`)
   - `anon public` key (under Project API keys)

### 4. Configure Local Environment
```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your credentials
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=your-anon-key-here
SECRET_KEY=any-random-string-for-development
```

### 5. Install & Run
```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

Visit `http://localhost:5000` 🎉

## ☁️ Deploy to Vercel

```bash
# Login to Vercel
vercel login

# Deploy
vercel

# Add environment variables in Vercel dashboard:
# - SUPABASE_URL
# - SUPABASE_KEY  
# - SECRET_KEY
```

Done! Your app is live.

## 📖 Need More Details?
See [SUPABASE_SETUP.md](SUPABASE_SETUP.md) for complete documentation.
