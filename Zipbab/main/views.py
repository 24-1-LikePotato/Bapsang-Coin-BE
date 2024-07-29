from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Ingredient, Recipe
from price.models import ChangePriceDay , ChangePriceMonth
from .serializers import IngredientSerializer,ChangePriceDaySerializer,RecipeSerializer , ChangePriceMonthSerializer
from rest_framework.decorators import api_view


    



@api_view(['GET'])
def ingredientsearch(request):
    query = request.GET.get('query','')
    if query:
        ingredient = Ingredient.objects.filter(name__icontains=query)
        if ingredient.exists():
            dayprice = ChangePriceDay.objects.filter(ingredient=ingredient)
            monthprice = ChangePriceMonth.objects.filter(ingredient=ingredient)
            if dayprice & monthprice:
                dayprice_serializer = ChangePriceDaySerializer(dayprice, many=True)
                monthprice_serializer = ChangePriceMonthSerializer(monthprice, many=True)
                return Response({"dayprice": dayprice_serializer.data, "monthprice" : monthprice_serializer.data})
    return Response({"error": "No data found"}, status=status.HTTP_404_NOT_FOUND)


    


    

# Create your views here.
