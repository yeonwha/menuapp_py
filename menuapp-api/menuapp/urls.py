from django.urls import path
from .views import FoodAPIController

urlpatterns=[
    path('menu', FoodAPIController.as_view()),
]