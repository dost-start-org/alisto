# Quick Start Guide

## First Time Setup

```bash
cd backend
./setup.sh
```

That's it! The script will:
- Start PostgreSQL container
- Create virtual environment
- Install dependencies
- Run migrations
- Offer to create superuser

## Daily Development

```bash
# Start database (if stopped)
docker compose up -d

# Activate virtual environment
source venv/bin/activate

# Start Django server
python manage.py runserver
```

## Useful Commands

| Task | Command |
|------|---------|
| Start PostgreSQL | `docker compose up -d` |
| Stop PostgreSQL | `docker compose down` |
| Activate venv | `source venv/bin/activate` |
| Start Django | `python manage.py runserver` |
| Make migrations | `python manage.py makemigrations` |
| Apply migrations | `python manage.py migrate` |
| Create superuser | `python manage.py createsuperuser` |
| Run tests | `python manage.py test` |
| DB shell | `docker exec -it postgres_db psql -U alisto_user -d postgres_db` |

## URLs

- API: http://localhost:8000
- Swagger: http://localhost:8000/swagger/
- Admin: http://localhost:8000/admin

## Troubleshooting

### Can't import Django
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Can't connect to database
```bash
docker compose up -d
docker ps  # Should show postgres_db
```

### Port 5433 busy
Edit `docker-compose.yml` and `.env` to use different port (e.g., 5434)

## Need More Help?

See detailed guides:
- **SETUP.md** - Complete setup instructions
- **README.md** - Project documentation
- **SETUP_SUMMARY.md** - What was fixed and why
