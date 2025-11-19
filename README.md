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
- **Database**: SQLite
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

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the app**
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

⚠️ **Database Limitation**: Vercel's serverless functions are stateless, so SQLite database will reset on each deployment. For production:

**Option 1: Use PostgreSQL (Recommended)**
- Add `psycopg2-binary` to `requirements.txt`
- Update database URI in `app.py`:
  ```python
  app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
  ```
- Add PostgreSQL database (Vercel Postgres, Neon, Supabase, etc.)

**Option 2: Use Vercel KV/Storage**
- Migrate to Vercel KV for persistence
- Requires code refactoring

**Option 3: External Database**
- Use Railway, PlanetScale, or MongoDB Atlas
- Update connection string in environment variables

### Environment Variables

Add to Vercel project settings:
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
├── requirements.txt       # Python dependencies
├── vercel.json           # Vercel deployment config
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
