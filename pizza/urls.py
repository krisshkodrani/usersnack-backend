from django.urls import path
from .views import PizzaReadOnlyModelViewSet, IngredientReadOnlyModelViewSet, OrderCreateAPIView

app_name = 'pizza'

urlpatterns = [
    path('', PizzaReadOnlyModelViewSet.as_view({'get': 'list'}), name='list'),
    path('<int:pk>/', PizzaReadOnlyModelViewSet.as_view({'get': 'retrieve'}), name='detail'),
    path('ingredients/', IngredientReadOnlyModelViewSet.as_view({'get': 'list'}), name='ingredient_list'),
    path('create-order/', OrderCreateAPIView.as_view(), name='create_order')
]
