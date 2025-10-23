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
                "hotline_number": seeder.faker.msisdn()[:11],
                "latitude": seeder.faker.latitude(),
                "longitude": seeder.faker.longitude(),
                "emergency_types": ["Fire", "Flood"]
            },
            {
                "name": "Philippine National Police",
                "logo_url": "https://pnp.gov.ph/wp-content/uploads/2022/03/cropped-logo_512.png",
                "hotline_number": seeder.faker.msisdn()[:11],
                "latitude": seeder.faker.latitude(),
                "longitude": seeder.faker.longitude(),
                "emergency_types": ["Active Crime"]
            },
            {
                "name": "Ambulance Service",
                "logo_url": "https://example.com/logos/ems.png",
                "hotline_number": seeder.faker.msisdn()[:11],
                "latitude": seeder.faker.latitude(),
                "longitude": seeder.faker.longitude(),
                "emergency_types": ["Medical Emergency"]
            },
            {
                "name": "Disaster Response Agency",
                "logo_url": "https://example.com/logos/dra.png",
                "hotline_number": seeder.faker.msisdn()[:11],
                "latitude": seeder.faker.latitude(),
                "longitude": seeder.faker.longitude(),
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