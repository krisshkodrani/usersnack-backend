from django.db import models


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    is_extra = models.BooleanField(default=False)
    price = models.FloatField(default=0.0)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Pizza(models.Model):
    name = models.CharField(max_length=200)
    base_price = models.FloatField()
    ingredients = models.ManyToManyField(Ingredient)
    image = models.ImageField(upload_to='images/', null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Order(models.Model):
    customer_name = models.CharField(max_length=200)
    customer_address = models.TextField()
    pizza = models.ForeignKey(Pizza, on_delete=models.SET_NULL, null=True)
    total = models.FloatField()
    metadata = models.JSONField(null=True)

    class Meta:
        ordering = ['customer_name']

    def __str__(self):
        return f"{self.customer_name}, {self.pizza} {self.total} USD"

