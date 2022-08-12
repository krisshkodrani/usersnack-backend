from django.contrib import admin
from . import models


@admin.register(models.Pizza)
class PizzaAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
