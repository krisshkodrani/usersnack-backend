from django.core.management.base import BaseCommand, CommandError
from pizza.models import Ingredient, Pizza, Order


class Command(BaseCommand):
    help = 'Easy delete seed data'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        Ingredient.objects.all().delete()
        for pizza in Pizza.objects.all():
            pizza.image.delete(save=False)  # delete file
            pizza.delete()
        Order.objects.all().delete()
        print('Deleted')
