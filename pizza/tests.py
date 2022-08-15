from django.shortcuts import resolve_url
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from pizza.management.commands.import_pizzas import import_pizzas, get_pizzas_and_extras, import_extras

from pizza.models import Pizza, Ingredient
from pizza.views import calculate_total


class PizzaOrderTestCase(TestCase):
    def setUp(self):
        pizzas, extras = get_pizzas_and_extras()
        import_pizzas(pizzas)
        import_extras(extras)
        self.extra_ham = Ingredient.objects.get(name='ham')
        self.extra_onion = Ingredient.objects.get(name='onion')
        self.extra_bacon = Ingredient.objects.get(name='bacon')
        self.extra_peppers = Ingredient.objects.get(name='green peppers')
        self.extra_mushrooms = Ingredient.objects.get(name='mushrooms')

    def test_calculate_base_pizza_price(self):
        # Cheese & Tomato
        pizza = Pizza.objects.get(id=1)
        total = calculate_total(pizza)
        self.assertEqual(pizza.base_price, total)
        # American Hot
        pizza = Pizza.objects.get(id=6)
        total = calculate_total(pizza)
        self.assertEqual(pizza.base_price, total)
        # Mighty Meaty
        pizza = Pizza.objects.get(id=2)
        total = calculate_total(pizza)
        self.assertEqual(pizza.base_price, total)

    def test_calculate_pizza_price_with_extra_ingredients(self):
        # Cheese & Tomato, extra ingredients onion 1 USD, mushrooms 1.2 USD
        pizza = Pizza.objects.get(id=1)
        extra = Ingredient.objects.filter(name__in=['onion', 'mushrooms'])
        total = calculate_total(pizza, extra)
        self.assertEqual(pizza.base_price + self.extra_onion.price + self.extra_mushrooms.price, total)
        # American Hot, extra ingredients bacon 2 USD, green peppers 1.2 USD
        pizza = Pizza.objects.get(id=6)
        extra = Ingredient.objects.filter(name__in=['bacon', 'green peppers'])
        total = calculate_total(pizza, extra)
        # Total is rounded to 2 decimal places
        self.assertAlmostEqual(pizza.base_price + self.extra_bacon.price + self.extra_peppers.price, total)


class PizzaAPITestCase(APITestCase):
    def setUp(self):
        pizzas, _ = get_pizzas_and_extras()
        import_pizzas(pizzas)

    def test_get_pizza_list(self):
        url = resolve_url('pizza:list')
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(14, len(response.data))

    def test_get_pizza_detail(self):
        url = resolve_url('pizza:detail', pk=1)
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual('Cheese & Tomato', response.data['name'])
        self.assertEqual(11.9, response.data['base_price'])
        self.assertEqual(2, len(response.data['ingredients']))
        self.assertIsNotNone(response.data['image'])


class IngredientAPIViewTestCase(APITestCase):
    def setUp(self):
        pizzas, extras = get_pizzas_and_extras()
        import_pizzas(pizzas)
        import_extras(extras)

    def test_get_ingredient_list(self):
        url = resolve_url('pizza:ingredient_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(18, len(response.data))

    def test_get_ingredient_list_is_extra(self):
        url = resolve_url('pizza:ingredient_list')
        response = self.client.get(url, {'is_extra': True})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(6, len(response.data))

        for ingredient in response.data:
            self.assertTrue(ingredient['price'] > 0)
