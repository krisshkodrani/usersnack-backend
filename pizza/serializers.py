from rest_framework import serializers
from .models import Pizza, Ingredient, Order


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name')


class PizzaSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True, allow_null=True)

    class Meta:
        model = Pizza
        fields = ('id', 'name', 'base_price', 'ingredients', 'image')


class OrderSerializer(serializers.ModelSerializer):
    pizza_id = serializers.Field()
    extra_ingredients = IngredientSerializer(many=True, allow_null=True)

    class Meta:
        model = Order
        fields = ('customer_name', 'customer_address', 'pizza_id', 'extra_ingredients',)
