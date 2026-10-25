# 📚 Knowledge Hub — Learning Log & Book Manager

A full-stack web application built with Django that helps users organize their learning journey, maintain personal learning logs, manage reading lists, and track book progress from a single dashboard.

## ✨ Features

### 🔐 User Authentication
- Create an account and log in securely.
- Manage personal learning logs and books.
- Keep each user's data private.

### 📊 Interactive Dashboard
- View totals for learning logs, books, and topics.
- Track learning activity over the last seven days.
- Monitor reading progress by book status.
- Access recently added logs and books.

### 📝 Learning Log Management
- Create, view, edit, and delete learning logs.
- Organize entries by topic.
- Add tags to categorize learning activities.
- Search logs by text, topic, and tag.
- Browse entries using pagination.

### 📖 Book Management
- Maintain a personal book collection.
- Organize books into **To Read**, **Reading**, and **Completed**.
- Record book titles, authors, categories, notes, and ratings.
- Search books and filter by category.
- Track reading progress from the dashboard.

### 🛡️ Security and Validation
- Django authentication and password hashing.
- Login protection for application pages.
- User-specific data access.
- Server-side form validation and CSRF protection.
- Protection against unauthorized access to other users' records.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Django 5.1 | Web framework |
| SQLite | Local development database |
| PostgreSQL | Production database support |
| HTML5 | Page structure |
| CSS3 | Styling and responsive layouts |
| Bootstrap 5.3 | UI components |
| JavaScript | Frontend interactions |
| WhiteNoise | Static file serving |
| Git and GitHub | Version control and source hosting |

## 📁 Project Structure

```text
knowledge_hub/
├── accounts/                 # Registration and authentication
├── books/                    # Book collection management
├── config/                   # Django settings and URL configuration
├── core/                     # Dashboard and shared utilities
├── logs/                     # Learning logs, topics, and tags
├── templates/                # HTML templates
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
├── .env.example              # Example environment configuration
├── .gitignore
├── manage.py
├── requirements.txt
├── requirements-prod.txt
└── README.md
```

## 🚀 Getting Started

Follow these instructions to run the project locally on Windows.

### Prerequisites

- Python 3.10 or newer
- Git
- Visual Studio Code (recommended)

### 1. Clone the repository

```bash
git clone https://github.com/manjunathgurupadappa-cloud/knowledge-hub.git
cd knowledge-hub
```

### 2. Create a virtual environment

```powershell
python -m venv venv
```

Activate it in PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution, run this in the current terminal and activate again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure environment variables (optional for local development)

Create a local environment file from the example:

```powershell
Copy-Item .env.example .env
```

Review `.env` and configure the settings required for your environment. Never commit real secrets or credentials.

### 5. Apply database migrations

```powershell
python manage.py makemigrations logs books
python manage.py migrate
```

### 6. Create demo data (optional)

```powershell
python manage.py create_demo_data
```

The demo-data command creates sample learning topics, logs, and books, along with a demo account. Use only the demo credentials documented in the command or its project documentation.

### 7. Create an administrator (optional)

```powershell
python manage.py createsuperuser
```

### 8. Run the development server

```powershell
python manage.py runserver
```

Open the application in your browser:

**http://127.0.0.1:8000/**

To access Django's admin interface:

**http://127.0.0.1:8000/admin/**

Press `Ctrl + C` in the terminal to stop the development server.

## 🧪 Running Tests

Run the automated Django tests with:

```powershell
python manage.py test
```

The test suite covers application behavior, including access protection and learning-log or book functionality.

You can also run Django's configuration checks:

```powershell
python manage.py check
```

## ⚙️ Configuration

The project supports environment-based configuration.

| Variable | Purpose |
|---|---|
| `DJANGO_DEBUG` | Enables or disables debug mode |
| `DJANGO_SECRET_KEY` | Django secret key |
| `DJANGO_ALLOWED_HOSTS` | Allowed hostnames |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | Trusted HTTPS origins |
| `DJANGO_TIME_ZONE` | Application time zone |
| `DATABASE_URL` | Database connection URL |

For production, set `DJANGO_DEBUG=False`, generate a unique secret key, configure allowed hosts and trusted origins, and use a properly configured production database.

Refer to `.env.example` for the available settings.

## ☁️ Deployment

The project includes production dependencies and WhiteNoise static-file support.

For a compatible hosting platform such as Render:

1. Push the project to GitHub.
2. Provision a PostgreSQL database.
3. Configure the required environment variables in the hosting dashboard.
4. Install the production dependencies and collect static files.
5. Apply database migrations.
6. Start the application using Gunicorn.

Example build command:

```bash
pip install -r requirements-prod.txt && python manage.py collectstatic --noinput && python manage.py migrate
```

Example start command:

```bash
gunicorn config.wsgi:application
```

Configure the database URL, secret key, allowed hosts, and CSRF trusted origins before deploying. Follow your hosting provider's instructions for environment variables and database networking.

**Note:** `python manage.py runserver` is intended for local development, not production hosting.

## 🔒 Security Notes

- Do not commit `.env` files or secret keys.
- Do not upload your virtual environment (`venv/`).
- Do not commit local databases containing private user information.
- Use HTTPS and secure production settings.
- Use strong passwords and protect production database credentials.

## 🎯 Project Goals

Knowledge Hub is designed to make personal learning more organized by combining learning notes, topic-based categorization, and book-progress tracking in one application.

It demonstrates practical skills in Django development, authentication, CRUD operations, relational database models, form validation, frontend integration, testing, and deployment configuration.

## 👨‍💻 Author

**Manjunath G**

GitHub: [@manjunathgurupadappa-cloud](https://github.com/manjunathgurupadappa-cloud)

## 📄 License

No license has been specified yet. If you intend to make this project open source, add a suitable `LICENSE` file and update this section.
