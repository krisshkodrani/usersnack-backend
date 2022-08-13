from django.core.management.base import BaseCommand, CommandError
from pizza.models import Ingredient, Pizza, Order


class Command(BaseCommand):
    help = 'Easy delete seed data'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        Ingredient.objects.all().delete()
        Pizza.objects.all().delete()
        Order.objects.all().delete()
        print('Deleted')
