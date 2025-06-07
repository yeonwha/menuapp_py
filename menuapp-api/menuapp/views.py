from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction 
from django.db.models import F 
from .models import Food
from .serializers import FoodSerializer

# Create and Retrieve the food list
class FoodListCreateAPIView(generics.ListCreateAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer

# Edit and Delete Food
class FoodRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer

# Handle applyDiscount patch calling to update all the selected foods.
# if the discount rate is out of range (0.1~0.9), no rate or selected food is provided, 
# Response 400 with error message.
class DiscountApplyAPIView(APIView):
    def patch(self, request, *args, **kwargs):
        discount_rate = request.data.get('rate')
        food_ids = request.data.get('foodIds')
    
        if discount_rate is None or not isinstance(discount_rate, (int, float)):
            return Response(
                {"error": "A valid 'rate' (e.g., 0.10 for 10%) is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not (0 <= discount_rate <= 1):
            return Response(
                {"error": "Discount rate must be between 0.1 and 0.9."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not isinstance(food_ids, list) or not all(isinstance(id, int) for id in food_ids):
            return Response(
                {"error": "A list of 'foodIds' (integers) is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not food_ids:
            return Response(
                {"message": "No food IDs provided to apply discount."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            with transaction.atomic():
                foods_to_update = Food.objects.filter(id__in=food_ids)

                if not foods_to_update.exists():
                    return Response(
                        {"message": "None of the provided food IDs were found."},
                        status=status.HTTP_404_NOT_FOUND
                    )

                # Total number of updated food items
                updated_count = foods_to_update.update(price=F('price') * (1 - discount_rate))

                # Update foods data
                updated_foods_data = FoodSerializer(foods_to_update, many=True).data

                # Response with the successful result
                return Response(
                    {
                        "message": f"Discount of {discount_rate*100:.0f}% applied to {updated_count} food items.",
                        "updated_count": updated_count,
                        "updated_foods_data": updated_foods_data
                    },
                    status=status.HTTP_200_OK
                )

        except Exception as err:
            return Response(
                {"error": f"Server error: {str(err)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )