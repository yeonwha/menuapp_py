from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction # Import transaction for atomicity
from django.db.models import F # Import F expression for database-level updates
from .models import Food
from .serializers import FoodSerializer

class FoodListCreateAPIView(generics.ListCreateAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer

class FoodRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer

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
            # 3. Get the food items that need to be updated
            # Filter by the provided foodIds
                foods_to_update = Food.objects.filter(id__in=food_ids)

                if not foods_to_update.exists():
                    return Response(
                        {"message": "None of the provided food IDs were found."},
                        status=status.HTTP_404_NOT_FOUND
                    )

            # 4. Apply the discount using F() expression for efficient bulk update
            # F('price') allows you to reference existing database field values
                updated_count = foods_to_update.update(price=F('price') * (1 - discount_rate))

            # Optional: Retrieve the updated foods to send their new prices back
            # This performs another query, but ensures you send fresh data.
            # If you only need a count, you can skip this.
                updated_foods_data = FoodSerializer(foods_to_update, many=True).data

                return Response(
                    {
                        "message": f"Discount of {discount_rate*100:.0f}% applied to {updated_count} food items.",
                        "updated_count": updated_count,
                        "updated_foods_data": updated_foods_data # Return updated data
                    },
                    status=status.HTTP_200_OK
                )

        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )