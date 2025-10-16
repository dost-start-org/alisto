"""
Django management command to create a superuser from environment variables.
Usage: python manage.py create_superuser_from_env
"""
import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Creates a superuser from environment variables if it does not exist'

    def handle(self, *args, **options):
        User = get_user_model()
        
        # Get credentials from environment variables
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
        first_name = os.environ.get('DJANGO_SUPERUSER_FIRST_NAME', 'Admin')
        last_name = os.environ.get('DJANGO_SUPERUSER_LAST_NAME', 'User')
        
        # Validate that all required variables are set
        if not email:
            self.stdout.write(
                self.style.ERROR('❌ DJANGO_SUPERUSER_EMAIL environment variable is not set')
            )
            return
        
        if not password:
            self.stdout.write(
                self.style.ERROR('❌ DJANGO_SUPERUSER_PASSWORD environment variable is not set')
            )
            return
        
        # Check if user already exists
        if User.objects.filter(email=email).exists():
            self.stdout.write(
                self.style.WARNING(f'⚠️  Superuser with email "{email}" already exists')
            )
            return
        
        # Create the superuser
        try:
            user = User.objects.create_superuser(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            self.stdout.write(
                self.style.SUCCESS(f'✅ Superuser "{email}" created successfully!')
            )
            self.stdout.write(
                self.style.SUCCESS(f'   Name: {first_name} {last_name}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error creating superuser: {str(e)}')
            )
