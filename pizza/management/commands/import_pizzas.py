from django.core.management.base import BaseCommand, CommandError
from pizza.models import Pizza

class Command(BaseCommand):
    help = 'Imports initial pizza data'

    def handle(self, *args, **options):
        pass