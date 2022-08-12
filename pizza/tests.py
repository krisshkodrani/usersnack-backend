from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status


class MakePizzaOrderTestCase(TestCase):
    def setUp(self):
        pass

    def test_make_pizza_order(self):
        pass


class PizzaViewsTestCase(APITestCase):
    def setUp(self):
        pass

    def test_get_pizza_list(self):
        url = reverse('pizza:list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
