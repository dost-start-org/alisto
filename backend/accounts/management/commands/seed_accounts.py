import random
from django.core.management.base import BaseCommand
from django_seed import Seed
from accounts.models import User, UserProfile  # adjust path as needed


class Command(BaseCommand):
    help = "Seed initial users: 2 Users and 1 Responder"

    def handle(self, *args, **options):
        seeder = Seed.seeder()

        # Authority and status choices
        status_choices = [choice[0] for choice in UserProfile.STATUS_CHOICES]

        # --- Create 2 regular Users ---
        for i in range(4):
            first_name = seeder.faker.first_name()
            last_name = seeder.faker.last_name()
            email = f"{first_name.lower()}.{last_name.lower()}@example.com"

            user = User.objects.create_user(
                email=email,
                password="password123",
                first_name=first_name,
                last_name=last_name,
            )

            UserProfile.objects.create(
                user=user,
                latitude=seeder.faker.latitude(),
                longitude=seeder.faker.longitude(),
                full_name=f"{first_name} {last_name}",
                authority_level="User",
                contact_number=seeder.faker.msisdn()[:11],
                date_of_birth=seeder.faker.date_of_birth(minimum_age=18, maximum_age=60),
                address=seeder.faker.address(),
                emergency_contact_name=seeder.faker.name(),
                emergency_contact_number=seeder.faker.msisdn()[:11],
                status=status_choices[i % len(status_choices)],
                email_verified=random.choice([True, False]),
            )
        
        # Create 4 Responders
        for i in range(4):
            first_name = seeder.faker.first_name()
            last_name = seeder.faker.last_name()
            email = f"{first_name.lower()}.{last_name.lower()}@responder.com"

            responder = User.objects.create_user(
                email=email,
                password="password123",
                first_name=first_name,
                last_name=last_name,
            )

            UserProfile.objects.create(
                user=responder,
                full_name=f"{first_name} {last_name}",
                authority_level="Responder",
                contact_number=seeder.faker.msisdn()[:11],
                date_of_birth=seeder.faker.date_of_birth(minimum_age=21, maximum_age=50),
                address=seeder.faker.address(),
                emergency_contact_name=seeder.faker.name(),
                emergency_contact_number=seeder.faker.msisdn()[:11],
                latitude=seeder.faker.latitude(),
                longitude=seeder.faker.longitude(),
                status="approved",
                email_verified=True,
            )

        self.stdout.write(self.style.SUCCESS("✅ Successfully seeded 4 Users and 4 Responders"))
