#!/bin/bash

# Alisto Backend Setup Script
# This script sets up the development environment for the first time

echo "🚀 Alisto Backend Setup"
echo "======================="
echo ""

# Check if we're in the backend directory
if [ ! -f "manage.py" ]; then
    echo "❌ Error: Please run this script from the backend directory"
    exit 1
fi

# Step 1: Start PostgreSQL Container
echo "📦 Step 1: Starting PostgreSQL container..."
if docker compose up -d 2>&1 | grep -q "Running\|Started\|Created"; then
    echo "✅ PostgreSQL container started"
else
    echo "⚠️  PostgreSQL container may already be running"
fi

# Wait for PostgreSQL to be ready
echo "⏳ Waiting for PostgreSQL to be ready..."
sleep 5

# Step 2: Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "🐍 Step 2: Creating virtual environment..."
    python3 -m venv venv
    if [ $? -eq 0 ]; then
        echo "✅ Virtual environment created"
    else
        echo "❌ Failed to create virtual environment"
        exit 1
    fi
else
    echo "✓ Virtual environment already exists"
fi

# Step 3: Activate virtual environment and install dependencies
echo "📚 Step 3: Installing dependencies..."
if [ -f "venv/bin/activate" ]; then
    # Use subshell to avoid affecting current shell
    (
        . venv/bin/activate
        pip install --upgrade pip
        pip install -r requirements.txt
    )
    if [ $? -eq 0 ]; then
        echo "✅ Dependencies installed"
    else
        echo "❌ Failed to install dependencies"
        exit 1
    fi
else
    echo "❌ Error: venv/bin/activate not found. Please delete venv directory and run again."
    exit 1
fi

# Step 4: Check environment file
if [ ! -f ".env" ]; then
    echo "⚙️  Step 4: Creating .env file from example..."
    cp .env.example .env
    echo "✅ .env file created"
    echo "⚠️  Please review .env file and update if needed"
else
    echo "✓ .env file already exists"
fi

# Step 5: Run migrations
echo "🗄️  Step 5: Running database migrations..."
if [ -f "venv/bin/python" ]; then
    venv/bin/python manage.py migrate
    if [ $? -eq 0 ]; then
        echo "✅ Migrations completed"
    else
        echo "❌ Failed to run migrations"
        exit 1
    fi
else
    echo "❌ Error: Python not found in virtual environment"
    exit 1
fi

# Step 6: Check if superuser should be created
echo ""
read -p "Would you like to create a superuser? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    venv/bin/python manage.py createsuperuser
fi

# Done!
echo ""
echo "✨ Setup complete!"
echo ""
echo "To start the development server:"
echo "  1. source venv/bin/activate"
echo "  2. python manage.py runserver"
echo ""
echo "API will be available at: http://localhost:8000"
echo "Swagger docs at: http://localhost:8000/swagger/"
echo "Admin panel at: http://localhost:8000/admin"
echo ""
echo "To stop PostgreSQL: docker compose down"
