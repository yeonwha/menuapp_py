from django.urls import path
from .views import FoodListCreateAPIView, FoodRetrieveUpdateDestroyAPIView, DiscountApplyAPIView

urlpatterns=[
    path('menu/', FoodListCreateAPIView.as_view(), name='food-list-create'),
    path('menu/<int:pk>/', FoodRetrieveUpdateDestroyAPIView.as_view(), name='food-detail'),
    path('menu/discount/', DiscountApplyAPIView.as_view()),
]