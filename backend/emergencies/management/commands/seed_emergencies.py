from django.core.management.base import BaseCommand
from emergencies.models import EmergencyType 

class Command(BaseCommand):
    help = "Seed initial emergency types"

    def handle(self, *args, **options):

        emergency_types = [
            {"name": "Fire", "icon_type": "fire"},
            {"name": "Flood", "icon_type": "flood"},
            {"name": "Medical Emergency", "icon_type": "medical"},
            {"name": "Active Crime", "icon_type": "crime"},
        ]

        for et in emergency_types:
            EmergencyType.objects.get_or_create(
                name=et["name"],
                icon_type=et["icon_type"]
            )

        self.stdout.write(self.style.SUCCESS("✅ Successfully seeded emergency types"))