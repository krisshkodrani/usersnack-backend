from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics, status
from django_filters import rest_framework as filters
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .models import Pizza, Ingredient, Order
from .serializers import PizzaSerializer, IngredientSerializer, OrderSerializer


def calculate_total(pizza: Pizza, extra_ingredients=None):
    if extra_ingredients is None:
        extra_ingredients = []

    total = pizza.base_price
    for i in extra_ingredients:
        total += i.price

    return round(total, 2)


class PizzaReadOnlyModelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Pizza.objects.all().order_by('id')
    serializer_class = PizzaSerializer


class IngredientReadOnlyModelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('is_extra',)


class OrderCreateAPIView(generics.GenericAPIView):
    serializer_class = OrderSerializer

    def post(self, request, *args, **kwargs):
        customer_name = self.get_required_field('customer_name')
        customer_address = self.get_required_field('customer_address')
        pizza = self.get_pizza()
        extra_ingredients = self.get_extra_ingredients()
        total = calculate_total(pizza, extra_ingredients)
        metadata = self.get_order_metadata(extra_ingredients)

        Order.objects.create(customer_name=customer_name,
                             customer_address=customer_address,
                             pizza=pizza,
                             total=total,
                             metadata=metadata)

        return Response({'success': True, 'base_price': pizza.base_price, 'total': total})

    def get_order_metadata(self, extra_ingredients):
        metadata = {}
        if extra_ingredients:
            extra_ingredients_ids = list(extra_ingredients.values_list('id', flat=True))
            metadata["extra_ingredients"] = extra_ingredients_ids
        return metadata

    def get_required_field(self, field_name):
        field_value = self.request.data.get(field_name)
        if not field_value:
            raise ValidationError({'detail': f"{field_name} is required"})
        return field_value

    def get_extra_ingredients(self):
        extra_ingredients = self.request.data.get('extra_ingredients', [])
        if extra_ingredients:
            extra_ingredient_ids = [int(i['id']) for i in extra_ingredients]
            return Ingredient.objects.filter(id__in=extra_ingredient_ids)
        return None

    def get_pizza(self):
        pizza_id = self.request.data.get('pizza_id')
        return get_object_or_404(Pizza, id=pizza_id, )
