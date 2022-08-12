from django.urls import path
from .views import PizzaListView

app_name = 'pizza'

urlpatterns = [
    path('', PizzaListView.as_view(), name='list')
]
