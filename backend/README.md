# How to run backend

## First time steps

> Starting from root project folder, using command prompt

1. `cd backend` to select backend folder
2. Copy `.env.example` to `.env` and update the values as needed (especially `DJANGO_SECRET_KEY`)
3. `python -m venv venv` to create a virtual environment named venv
4. `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Linux/Mac) to enter the virtual environment
5. `pip install -r requirements.txt` to install dependencies
6. `python manage.py makemigrations` and then `python manage.py migrate` to initialize database migrations
7. `python manage.py runserver` to run the backend server locally

## Production Deployment

This application is configured to run in production environments using Gunicorn WSGI server.

### Digital Ocean App Platform Deployment

#### Required Configuration

1. **Build Command**:

   ```
   python manage.py collectstatic --noinput
   ```

2. **Run Command**:

   ```
   gunicorn nstw_backend.wsgi:application --bind 0.0.0.0:$PORT --workers 3
   ```

3. **Environment Variables**:
   - `DJANGO_SECRET_KEY`: Your secure secret key
   - `DJANGO_DEBUG`: Set to `False` for production
   - `ALLOWED_HOSTS`: Include your Digital Ocean app URL (e.g., `yourapp.ondigitalocean.app`)
   - Other environment variables as specified in `.env.example`

#### Database Migration

After deployment, you may need to run database migrations:

1. Go to your App Platform console
2. Access the Console tab
3. Run: `python manage.py migrate`

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
