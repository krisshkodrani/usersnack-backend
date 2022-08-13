import json
import os

from django.core.files import File
from django.core.management.base import BaseCommand, CommandError
from pizza.models import Pizza, Ingredient


def price_to_money(price):
    return round(float(price), 2)


def import_pizzas(pizzas):
    for p in pizzas:
        ingredients = []
        for pi in p['ingredients']:
            ingredient, _ = Ingredient.objects.get_or_create(name=pi)
            ingredients.append(ingredient)

        pizza = Pizza.objects.create(id=p['id'], name=p['name'], base_price=price_to_money(p['price']))
        pizza.ingredients.add(*ingredients)
        img_file = p['img']
        pizza.image.save(os.path.basename(img_file), File(open(f"pizza/management/resources/img/{img_file}", 'rb')))


def import_extras(extras):
    for e in extras:
        ingredient, _ = Ingredient.objects.get_or_create(name=e['name'])
        ingredient.price = price_to_money(e['price'])
        ingredient.is_extra = True
        ingredient.save()


def get_pizzas_and_extras():
    data = open('pizza/management/resources/data.json')
    data = json.load(data)
    return data["Pizzas"], data["Extras"]


class Command(BaseCommand):
    help = 'Imports initial pizza data'

    def handle(self, *args, **options):
        pizzas, extras = get_pizzas_and_extras()

        import_extras(extras)
        import_pizzas(pizzas)
