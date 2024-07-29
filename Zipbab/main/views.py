from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Ingredient, Recipe
from price.models import ChangePriceDay,ChangePriceMonth
from .serializers import IngredientSerializer,ChangePriceDaySerializer,RecipeSerializer,ChangePriceMonthSerializer
from rest_framework.decorators import api_view

# Create your views here.
@api_view(['GET'])
def ingredientpage(request):
    dayprice = ChangePriceDay.objects.order_by('price').first()
    monthprice = ChangePriceMonth.objects.order_by('today').first()
    if dayprice & monthprice:
        dayprice_serializer = ChangePriceDaySerializer(dayprice, many=True)
        monthprice_serializer = ChangePriceMonthSerializer(monthprice, many=True)
        return Response({"dayprice": dayprice_serializer.data, "monthprice" : monthprice_serializer.data})
    return Response({"error": "No data found"}, status=status.HTTP_404_NOT_FOUND)



