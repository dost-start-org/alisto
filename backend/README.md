# Alisto Backend

Django REST API backend for the Alisto emergency response system.

## Prerequisites

- Python 3.13+
- PostgreSQL (via Docker)
- pip package manager

## Quick Start

### 1. Start PostgreSQL Database

```bash
# From the backend directory
docker compose up -d
```

This starts PostgreSQL on port 5433.

### 2. Set Up Python Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env if needed (defaults should work for local development)
```

### 4. Initialize Database

```bash
# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser
```

### 5. Start Django Server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000`

## Architecture

**Setup**: Dockerized PostgreSQL + Local Django Development

- **Database**: PostgreSQL runs in Docker container (port 5433)
- **Django**: Runs locally in virtual environment (port 8000)
- **Connection**: Django connects to `localhost:5433` to access containerized PostgreSQL

## Project Structure

```
backend/
├── accounts/          # User authentication and profiles
├── agencies/          # Emergency response agencies
├── emergencies/       # Emergency types and incidents
├── public_info/       # Public emergency contacts
├── responders/        # Emergency responders
├── nstw_backend/      # Main Django settings
├── docker-compose.yml # PostgreSQL container config
├── requirements.txt   # Python dependencies
├── .env              # Environment variables (local dev)
└── manage.py         # Django management script
```

## Environment Variables

Key environment variables in `.env`:

```bash
# Django Configuration
DJANGO_SECRET_KEY='your-secret-key-here'
ALLOWED_HOSTS=localhost,127.0.0.1
DJANGO_DEBUG=True

# PostgreSQL (connects to Docker container)
POSTGRES_DB=postgres_db
POSTGRES_USER=alisto_user
POSTGRES_PASSWORD=alisto_password
DB_HOST=localhost      # localhost for local Django
DB_PORT=5433          # mapped port from Docker

# Frontend
FRONTEND_URL=http://localhost:3000
DEFAULT_FROM_EMAIL=noreply@example.com
```

## Common Commands

```bash
# Database Operations
python manage.py makemigrations    # Create new migrations
python manage.py migrate           # Apply migrations
python manage.py createsuperuser   # Create admin user

# Development
python manage.py runserver         # Start dev server
python manage.py test             # Run tests
python manage.py check            # Check for issues

# Static Files
python manage.py collectstatic    # Collect static files
```

## Database Management

### Access PostgreSQL Shell

```bash
# Via Docker
docker exec -it postgres_db psql -U alisto_user -d postgres_db

# List tables
\dt

# Exit
\q
```

### Reset Database

```bash
# Stop and remove containers
docker compose down

# Remove volume (deletes all data!)
docker volume rm backend_postgres_db

# Start fresh
docker compose up -d
python manage.py migrate
```

## API Documentation

Once the server is running:

- **Swagger UI**: http://localhost:8000/swagger/
- **ReDoc**: http://localhost:8000/redoc/

## Troubleshooting

### Cannot connect to database

1. **Check if container is running**:

   ```bash
   docker ps
   ```

2. **Check container logs**:

   ```bash
   docker logs postgres_db
   ```

3. **Verify environment variables** in `.env`:
   - `DB_HOST=localhost`
   - `DB_PORT=5433`

### Module not found errors

```bash
# Make sure virtual environment is activated
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Port already in use

If port 5433 is busy, edit `docker-compose.yml`:

```yaml
ports:
  - "5434:5432" # Change to different port
```

Then update `DB_PORT=5434` in `.env`

## Production Deployment

### Digital Ocean App Platform

**Build Command**:

```bash
python manage.py collectstatic --noinput
```

**Run Command**:

```bash
gunicorn nstw_backend.wsgi:application --bind 0.0.0.0:$PORT --workers 3
```

3. **Environment Variables**:
   - `DJANGO_SECRET_KEY`: Your secure secret key
   - `DJANGO_DEBUG`: Set to `False` for production
   - `ALLOWED_HOSTS`: Include your Digital Ocean app URL (e.g., `yourapp.ondigitalocean.app`)
   - `DJANGO_SUPERUSER_EMAIL`: Admin email (e.g., `admin@example.com`)
   - `DJANGO_SUPERUSER_PASSWORD`: Secure admin password
   - `DJANGO_SUPERUSER_FIRST_NAME`: (Optional) Admin first name (default: `Admin`)
   - `DJANGO_SUPERUSER_LAST_NAME`: (Optional) Admin last name (default: `User`)
   - Other environment variables as specified in `.env.example`

#### Database Migration

After deployment, you may need to run database migrations:

1. Go to your App Platform console
2. Access the Console tab
3. Run: `python manage.py migrate`

#### Creating Superuser on Staging/Production

**Option 1: Using Environment Variables (Recommended)**

Set these environment variables in your hosting platform:

```bash
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=your-secure-password
DJANGO_SUPERUSER_FIRST_NAME=Admin  # Optional
DJANGO_SUPERUSER_LAST_NAME=User    # Optional
```

Then run:

```bash
python manage.py create_superuser_from_env
```

This command will create the superuser if it doesn't already exist. It's safe to run multiple times.

**Option 2: Interactive Creation**

Access your server console and run:

```bash
python manage.py createsuperuser
```

Follow the prompts to create the superuser interactively.

### Manual Production Deployment

If deploying to a VPS or other platform manually:

1. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

2. Set up environment variables or create a `.env` file (use `.env.example` as a template)

3. Run the production startup script:
   ```
   ./start_production.sh
   ```

This will collect static files, apply migrations, and start the Gunicorn server.
