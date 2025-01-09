from django.core.management.base import BaseCommand
from profile_manager.db_company_processor import process_company_information

class Command(BaseCommand):
    help = 'Run the process_company_information script'

    def handle(self, *args, **kwargs):
        process_company_information()