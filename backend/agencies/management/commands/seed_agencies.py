import random
from django.core.management.base import BaseCommand
from django_seed import Seed
from agencies.models import Agency, AgencyEmergencyType
from emergencies.models import EmergencyType

class Command(BaseCommand):
    help = "Seed initial agencies and their emergency types"

    def handle(self, *args, **options):
        seeder = Seed.seeder()

        # Predefined agencies data
        agencies_data = [
            {
                "name": "Bureau of Fire Protection",
                "logo_url": "https://bfp.gov.ph/wp-content/uploads/2023/04/BFP-OFFICIAL-LOGO.png",
                "hotline_number": "123-456-7890",
                "latitude": 40.7128,
                "longitude": -74.0060,
                "emergency_types": ["Fire", "Flood"]
            },
            {
                "name": "Philippine National Police",
                "logo_url": "https://pnp.gov.ph/wp-content/uploads/2022/03/cropped-logo_512.png",
                "hotline_number": "098-765-4321",
                "latitude": 34.0522,
                "longitude": -118.2437,
                "emergency_types": ["Active Crime"]
            },
            {
                "name": "Ambulance Service",
                "logo_url": "https://example.com/logos/ems.png",
                "hotline_number": "555-555-5555",
                "latitude": 41.8781,
                "longitude": -87.6298,
                "emergency_types": ["Medical Emergency"]
            },
            {
                "name": "Disaster Response Agency",
                "logo_url": "https://example.com/logos/dra.png",
                "hotline_number": "444-444-4444",
                "latitude": 29.7604,
                "longitude": -95.3698,
                "emergency_types": ["Flood", "Fire", "Medical Emergency"]
            },
        ]

        for agency_data in agencies_data:
            agency, created = Agency.objects.get_or_create(
                name=agency_data["name"],
                defaults={
                    "logo_url": agency_data["logo_url"],
                    "hotline_number": agency_data["hotline_number"],
                    "latitude": agency_data["latitude"],
                    "longitude": agency_data["longitude"],
                }
            )

            for et_name in agency_data["emergency_types"]:
                try:
                    emergency_type = EmergencyType.objects.get(name=et_name)
                    AgencyEmergencyType.objects.get_or_create(
                        agency=agency,
                        emergency_type=emergency_type
                    )
                except EmergencyType.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f"⚠️ EmergencyType '{et_name}' not found. Skipping."))


        self.stdout.write(self.style.SUCCESS("✅ Successfully seeded agencies and their emergency types"))