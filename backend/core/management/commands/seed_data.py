from django.core.management.base import BaseCommand
from accounts.management.commands import seed_accounts
from emergencies.management.commands import seed_emergencies
from agencies.management.commands import seed_agencies
from public_info.management.commands import seed_publicinfo
from responders.management.commands import seed_responders
class Command(BaseCommand):
    help = "Seed data for all apps"

    def handle(self, *args, **options):
        seed_accounts.Command().handle()
        seed_emergencies.Command().handle()
        seed_agencies.Command().handle()
        seed_publicinfo.Command().handle()
        seed_responders.Command().handle()

        self.stdout.write(self.style.SUCCESS('✅ All data seeded successfully!'))
