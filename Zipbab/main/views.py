from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Ingredient, Recipe
from price.models import ChangePriceDay
from .serializers import IngredientSerializer,ChangePriceDaySerializer,RecipeSerializer
from rest_framework.decorators import api_view
# Create your views here.
@api_view(['GET'])
def ingredientpage(request):
    changeprice = ChangePriceDay.objects.order_by('price').first()
    if changeprice:
        serializer = ChangePriceDaySerializer(changeprice)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({"error": "No data found"}, status=status.HTTP_404_NOT_FOUND)

    



