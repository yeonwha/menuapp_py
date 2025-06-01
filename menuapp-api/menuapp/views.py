from rest_framework import generics
from .models import Food
from .serializers import FoodSerializer

class FoodAPIController(generics.ListCreateAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer