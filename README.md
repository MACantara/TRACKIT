# TRACKIT - Personal Finance Tracker

**Tracking Real Time Accounts, Costs, and Keeping It Tidy**

A responsive Progressive Web App (PWA) built with Flask for managing personal finances, tracking accounts, transactions, and budgets.

## 🚀 Features

- **Dashboard** - Overview of total balance, income, expenses, and accounts
- **Account Management** - Track multiple accounts (Checking, Savings, Credit Card, etc.)
- **Transaction Tracking** - Record income and expenses with categories
- **Budget Management** - Set spending limits and monitor usage
- **Progressive Web App** - Install on mobile/desktop, works offline
- **Responsive Design** - Beautiful UI with Tailwind CSS
- **Real-time Updates** - Automatic balance calculations

## 🛠️ Tech Stack

- **Backend**: Python, Flask, SQLAlchemy
- **Database**: Supabase PostgreSQL (production) / SQLite (local dev)
- **Frontend**: HTML, Tailwind CSS v4, Bootstrap Icons
- **PWA**: Service Worker, Web Manifest

## 📦 Installation

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/MACantara/TRACKIT.git
   cd TRACKIT
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure database (choose one)**

   **Option A: SQLite (Quick Start)**
   - No setup needed! App will use SQLite by default
   - Perfect for local development and testing

   **Option B: Supabase PostgreSQL (Production)**
   - See [SUPABASE_SETUP.md](SUPABASE_SETUP.md) for detailed instructions
   - Copy `.env.example` to `.env` and add your Supabase credentials
   - Run `supabase_schema.sql` in Supabase SQL Editor

6. **Run the application**
   ```bash
   python app.py
   ```

7. **Access the app**
   - Open your browser to `http://localhost:5000`

### Seed Sample Data (Optional)

```bash
python scripts/seed_data.py --reset
```

This creates sample accounts, transactions, and budgets for testing.

## 🌐 Deploying to Vercel

### Prerequisites
- Vercel account (free tier works)
- Vercel CLI installed: `npm i -g vercel`

### Deployment Steps

1. **Login to Vercel**
   ```bash
   vercel login
   ```

2. **Deploy**
   ```bash
   vercel
   ```

3. **Follow prompts**
   - Link to existing project or create new
   - Confirm settings
   - Deploy!

### Important Notes for Vercel

✅ **Supabase PostgreSQL Integration**: The app now supports Supabase PostgreSQL for production deployments!

**Setup Steps:**
1. Create a Supabase project and run `supabase_schema.sql`
2. Get your credentials from Supabase dashboard
3. Add environment variables to Vercel (see below)

For detailed instructions, see [SUPABASE_SETUP.md](SUPABASE_SETUP.md)

### Environment Variables

Add to Vercel project settings:
```
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=your-anon-key-here
DATABASE_URL=postgresql://postgres:password@db.xxxxx.supabase.co:5432/postgres
SECRET_KEY=your-secure-random-key-here
```
```
SECRET_KEY=your-secure-random-key-here
DATABASE_URL=postgresql://...  # If using PostgreSQL
```

## 📱 PWA Installation

### Mobile (iOS/Android)
1. Visit the deployed URL in mobile browser
2. Look for "Add to Home Screen" prompt
3. Tap to install

### Desktop (Chrome/Edge)
1. Visit the site
2. Click install icon in address bar
3. Or: Browser menu → "Install TRACKIT..."

## 📂 Project Structure

```
TRACKIT/
├── app.py                 # Main Flask application
├── database.py            # Supabase/PostgreSQL integration
├── requirements.txt       # Python dependencies
├── vercel.json           # Vercel deployment config
├── supabase_schema.sql   # Database schema for Supabase
├── .env.example          # Environment variables template
├── SUPABASE_SETUP.md     # Detailed Supabase setup guide
├── templates/            # HTML templates
│   ├── base.html        # Base layout with PWA support
│   ├── index.html       # Dashboard
│   ├── accounts.html    # Account management
│   ├── transactions.html # Transaction tracking
│   └── budgets.html     # Budget management
├── static/              # Static files
│   ├── manifest.json    # PWA manifest
│   ├── service-worker.js # Service worker for offline
│   └── icons/           # PWA icons
├── scripts/             # Utility scripts
│   ├── seed_data.py     # Sample data generator
│   └── generate_icons.py # Icon generator
└── trackit.db           # SQLite database (local only)
```

## 🎨 Customization

### Icons
Generate better icons with Pillow:
```bash
pip install Pillow
python scripts/generate_icons.py
```

### Colors
Edit `base.html` and `manifest.json` to change theme colors.

### Features
- Add more transaction categories in forms
- Implement data export/import
- Add charts and visualizations
- Multi-user support with authentication

## 📝 API Endpoints

- `GET /` - Dashboard
- `GET /accounts` - Account list
- `POST /account/add` - Create account
- `DELETE /account/delete/<id>` - Delete account
- `GET /transactions` - Transaction list
- `POST /transaction/add` - Create transaction
- `DELETE /transaction/delete/<id>` - Delete transaction
- `GET /budgets` - Budget list
- `POST /budget/add` - Create/update budget
- `DELETE /budget/delete/<id>` - Delete budget
- `GET /api/stats` - Get statistics (JSON)

## 🤝 Contributing

Contributions welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 👤 Author

**MACantara**
- GitHub: [@MACantara](https://github.com/MACantara)

## 🙏 Acknowledgments

- Tailwind CSS for beautiful styling
- Bootstrap Icons for iconography
- Flask community for excellent documentation

---

**TRACKIT** - Keep your finances organized and tidy! 💰📊
