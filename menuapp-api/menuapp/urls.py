from django.urls import path
from .views import FoodListCreateAPIView, FoodRetrieveUpdateDestroyAPIView, DiscountApplyAPIView

urlpatterns=[
    # Create and Retrieve food
    path('menu/', FoodListCreateAPIView.as_view(), name='food-list-create'),

    # Update food's price and Delete food
    path('menu/<int:pk>/', FoodRetrieveUpdateDestroyAPIView.as_view(), name='food-detail'),

    # Bulk update to apply discount rate
    path('menu/discount/', DiscountApplyAPIView.as_view()),
]