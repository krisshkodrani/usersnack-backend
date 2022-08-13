from django.contrib import admin
from . import models


@admin.register(models.Pizza)
class PizzaAdmin(admin.ModelAdmin):
    list_display = ('name', 'base_price', 'id')


@admin.register(models.Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_extra')


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'pizza_id', 'id')
