import random
from django.core.management.base import BaseCommand
from django_seed import Seed
from accounts.models import UserProfile
from agencies.models import Agency
from responders.models import Responder  # adjust app name if different


class Command(BaseCommand):
    help = "Link existing responder users to agencies"

    def handle(self, *args, **options):
        seeder = Seed.seeder()

        # Fetch all responders (authority_level = 'Responder')
        responders = UserProfile.objects.filter(authority_level="Responder")

        # Fetch all agencies
        agencies = list(Agency.objects.all())

        # Randomly assign each responder to an agency (1:1 mapping)
        for responder_profile in responders:
            user = responder_profile.user

            # Pick a random agency that isn’t already assigned to this responder (unique_together constraint)
            agency = random.choice(agencies)

            # Create or skip if already exists
            responder_obj, created = Responder.objects.get_or_create(
                user=user,
                agency=agency,
            )

        self.stdout.write(self.style.SUCCESS("✅ Successfully seeded responder-agency links"))
