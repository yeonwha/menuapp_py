from django.urls import path
from .views import FoodAPIController

urlpatterns=[
    path('menu', FoodAPIController.as_view()),
    path('menu/<int:food_id>', FoodPriceEdit),
    path('menu/<int:food_id>', FoodDeleteController)
    patch('menu/discount', FoodApplyDiscount),
]