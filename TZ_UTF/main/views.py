from django.db.models import Count, Q, Prefetch
from django.http import HttpRequest, JsonResponse
from rest_framework.views import APIView

from main.models import Food, FoodCategory, FoodListSerializer


class TZ_View(APIView):
    def get(self, request: HttpRequest):

        published_food = Food.objects.filter(is_publish=True)
        food_category = FoodCategory.objects.annotate(published_dish_counter=Count(
            'food', filter=Q(food__is_publish=True))).filter(published_dish_counter__gt=0).prefetch_related(
            Prefetch('food', queryset=published_food))
        food_serializer = FoodListSerializer(food_category, many=True)
        food_response = food_serializer.data

        return JsonResponse(food_response, safe=False)
