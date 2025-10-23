import random
from django.core.management.base import BaseCommand
from django_seed import Seed
from public_info.models import EmergencyContact, ContactRedirection
from emergencies.models import EmergencyType

class Command(BaseCommand):
    help = "Seed initial emergency contacts and their redirections"

    def handle(self, *args, **options):
        seeder = Seed.seeder()
        
        # Predefined emergency contacts data
        contacts_data = [
            {
                "name": "Bureau of Fire Protection Hotline",
                "contact_number": seeder.faker.msisdn()[:11],
                "description": "Contact for fire emergencies",
                "type": "Hotline",
                "emergency_types": ["Fire"]
            },
            {
                "name": "Local Ambulance Service",
                "contact_number": seeder.faker.msisdn()[:11],
                "description": "Contact for medical emergencies",
                "type": "Hotline",
                "emergency_types": ["Medical Emergency"]
            },
            {
                "name": "Police Emergency Hotline",
                "contact_number": seeder.faker.msisdn()[:11],
                "description": "General contact for all emergencies",
                "type": "General Contact",
                "emergency_types": ["Fire", "Flood", "Medical Emergency", "Active Crime"]
            },
        ]

        for contact_data in contacts_data:
            contact, created = EmergencyContact.objects.get_or_create(
                name=contact_data["name"],
                contact_number=contact_data["contact_number"],
                defaults={
                    "description": contact_data["description"],
                    "type": contact_data["type"],
                }
            )

            for et_name in contact_data["emergency_types"]:
                try:
                    emergency_type = EmergencyType.objects.get(name=et_name)
                    ContactRedirection.objects.get_or_create(
                        contact=contact,
                        emergency_type=emergency_type
                    )
                except EmergencyType.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f"⚠️ EmergencyType '{et_name}' not found. Skipping."))

        self.stdout.write(self.style.SUCCESS("✅ Successfully seeded emergency contacts and their redirections"))