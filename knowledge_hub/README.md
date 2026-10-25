# Knowledge Hub - Learning Log & Book Manager

A full-stack Django app where each user keeps private **learning logs** (with topics and tags)
and a **book shelf** (To Read / Reading / Completed, ratings, notes).

**Stack:** Python 3.10+, Django 5.1, SQLite (PostgreSQL in production), Bootstrap 5.3, vanilla JavaScript.

> The page loads Bootstrap, Bootstrap Icons and Google Fonts from a CDN, so you need an internet
> connection in the browser the first time you open it.

---

## Folder structure

```
knowledge_hub/
├── manage.py
├── requirements.txt          # local + base dependencies
├── requirements-prod.txt     # adds gunicorn + PostgreSQL driver for hosting
├── .env.example              # copy to .env
├── .gitignore
├── README.md
├── config/                   # project settings, urls, wsgi/asgi
├── core/                     # dashboard, shared form mixin, pagination, demo-data command
│   └── management/commands/create_demo_data.py
├── accounts/                 # register / login / logout
├── logs/                     # Topic, Tag, LearningLog (models, forms, views, tests)
├── books/                    # Book (models, forms, views, tests)
├── templates/                # base, layout (sidebar), auth, form_page, confirm_delete, per-app pages
└── static/
    ├── css/style.css
    └── js/app.js
```

---

## Run locally on Windows (PowerShell)

### 1. Install the tools
* Python 3.10 or newer from https://www.python.org/downloads/ (tick **Add python.exe to PATH**).
* VS Code from https://code.visualstudio.com/ and its **Python** extension (Microsoft).

Check Python:
```powershell
python --version
```

### 2. Open the project in VS Code
1. Unzip `knowledge_hub.zip`.
2. VS Code -> **File -> Open Folder...** -> choose the `knowledge_hub` folder.
3. Open the terminal: **Terminal -> New Terminal** (it should be PowerShell and already inside `knowledge_hub`).

### 3. Create and activate a virtual environment
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```
If PowerShell says scripts are disabled, run this once, then activate again:
```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```
Your prompt should now start with `(venv)`.

In VS Code press **Ctrl+Shift+P -> "Python: Select Interpreter"** and choose the one inside `.\venv`.

### 4. Install dependencies
```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 5. (Optional) Environment file
Local development works without it. To create one anyway:
```powershell
Copy-Item .env.example .env
```

### 6. Create the database (migrations)
The migration files are generated from the models on your machine:
```powershell
python manage.py makemigrations logs books
python manage.py migrate
```
This creates `db.sqlite3`.

### 7. Load demo data (optional but recommended)
```powershell
python manage.py create_demo_data
```
Creates user **demo** / password **demo12345** with 4 topics, 10 logs and 7 books.
Re-create it from scratch with `python manage.py create_demo_data --reset`.
Custom user: `python manage.py create_demo_data --username sam --password MyPass12345`.

### 8. (Optional) Create an admin user
```powershell
python manage.py createsuperuser
```

### 9. Start the server
```powershell
python manage.py runserver
```
Open http://127.0.0.1:8000/ and log in (or click **Create an account**).
Stop the server with **Ctrl+C**. Admin site: http://127.0.0.1:8000/admin/

### 10. Run the automated tests
```powershell
python manage.py test
```
The tests check login protection, that one user cannot see/edit/delete another user's data,
tag handling, filtering and validation.

### Running from VS Code's Run button (optional)
Create `.vscode/launch.json`:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Django: runserver",
      "type": "debugpy",
      "request": "launch",
      "program": "${workspaceFolder}/manage.py",
      "args": ["runserver"],
      "django": true
    }
  ]
}
```
Press **F5** to run with breakpoints.

---

## Features

| Area | What you get |
|------|--------------|
| Auth | Register, login, logout (Django auth, hashed passwords, password validators, CSRF) |
| Dashboard | Totals for logs / books / topics, logs in the last 7 days, reading progress, recent logs and books, logs by topic |
| Learning logs | Create, view, edit, delete; search by text/topic/tag; tag chips; pagination |
| Topics | Add, rename, delete (blocked while a topic still has logs) |
| Books | Add, view, edit, delete; status tabs with counts; search; category filter; 1-5 rating |
| Security | `@login_required` on every page; every query filtered by `request.user`; other users' objects return 404; server-side validation in Django forms; delete only via POST |

### Validation rules
* Log title: at least 3 characters. Date cannot be in the future. Max 10 tags of up to 30 characters.
* Topic names are unique per user (case-insensitive).
* A book in "To Read" cannot have a rating.

---

## Configuration (environment variables)

| Variable | Purpose | Default (local) |
|----------|---------|-----------------|
| `DJANGO_DEBUG` | `True` for development, **`False` in production** | `True` |
| `DJANGO_SECRET_KEY` | Secret signing key (**required when DEBUG is False**) | built-in dev key |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated host names | `localhost,127.0.0.1` |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | Your site URL(s) incl. `https://` | empty |
| `DJANGO_TIME_ZONE` | e.g. `Asia/Kolkata` | `UTC` |
| `DATABASE_URL` | PostgreSQL URL; empty = SQLite | empty |
| `DATABASE_SSL_REQUIRE` | `True` if your provider requires SSL | `False` |
| `DJANGO_SECURE_SSL_REDIRECT` | Redirect HTTP to HTTPS when DEBUG is False | `True` |
| `DJANGO_HSTS_SECONDS` | HSTS duration; start with `0`, then raise (e.g. `31536000`) | `0` |

Generate a secret key in PowerShell:
```powershell
python -c "from django.core.management.utils import get_random_secret_key as g; print(g())"
```

---

## Deploying to a cloud host (example: Render)

The same steps work on Railway, Fly.io, Heroku-style hosts, or any VPS - only the dashboard differs.

1. **Commit the migrations** (they were created in step 6) and push the project to GitHub.
   `db.sqlite3`, `.env` and `venv/` are ignored by `.gitignore`.
2. **Create a PostgreSQL database** on the host. Copy its *Internal/External Database URL*.
3. **Create a Web Service** from your repo with:
   * Build command:
     ```
     pip install -r requirements-prod.txt && python manage.py collectstatic --noinput && python manage.py migrate
     ```
   * Start command:
     ```
     gunicorn config.wsgi:application
     ```
4. **Set environment variables** on the service:
   ```
   DJANGO_DEBUG=False
   DJANGO_SECRET_KEY=<generated key>
   DJANGO_ALLOWED_HOSTS=your-app.onrender.com
   DJANGO_CSRF_TRUSTED_ORIGINS=https://your-app.onrender.com
   DATABASE_URL=<your PostgreSQL URL>
   ```
5. Deploy, then create your admin user from the host's shell:
   `python manage.py createsuperuser`

Static files are served by WhiteNoise (already configured), so no separate static host is needed.

### PostgreSQL locally (optional)
SQLite stays the default. To test against PostgreSQL on your machine:
```powershell
pip install -r requirements-prod.txt
$env:DATABASE_URL = "postgres://USER:PASSWORD@localhost:5432/knowledge_hub"
python manage.py migrate
python manage.py runserver
```
(`$env:` only lasts for that PowerShell window. Or put `DATABASE_URL=...` in `.env`.)

### Production checklist
- [ ] `DJANGO_DEBUG=False` and a unique `DJANGO_SECRET_KEY`
- [ ] `DJANGO_ALLOWED_HOSTS` and `DJANGO_CSRF_TRUSTED_ORIGINS` match your domain
- [ ] PostgreSQL `DATABASE_URL` set; automatic backups enabled on the host
- [ ] `python manage.py check --deploy` shows no serious warnings
- [ ] Raise `DJANGO_HSTS_SECONDS` once HTTPS works

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `python` not found | Reinstall Python and tick "Add to PATH", or use `py` instead of `python` |
| `Activate.ps1 cannot be loaded` | Run the `Set-ExecutionPolicy` command in step 3 |
| `No module named 'django'` | Activate the venv (`.\venv\Scripts\Activate.ps1`) and run `pip install -r requirements.txt` |
| `no such table` error | Run `python manage.py makemigrations logs books` then `python manage.py migrate` |
| Page looks unstyled | The browser needs internet access for the Bootstrap CDN |
| `Port already in use` | `python manage.py runserver 8001` |
| CSRF error in production | Add your `https://` URL to `DJANGO_CSRF_TRUSTED_ORIGINS` |
