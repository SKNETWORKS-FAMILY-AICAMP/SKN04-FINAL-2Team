from django.core.management.base import BaseCommand
from profile_manager import db_input_processor

class Command(BaseCommand):
    help = 'Run the db_input_processor script'

    def handle(self, *args, **kwargs):
        result = db_input_processor.db_input_processor(start_index=0)
        print(result)