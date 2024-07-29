from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Ingredient, Recipe
from price.models import ChangePriceDay
from .serializers import IngredientSerializer,ChangePriceDaySerializer,RecipeSerializer
from rest_framework.decorators import api_view


    


@api_view(['GET'])
def recipesearch(request):
    query = request.GET.get('query','')
    if query:
        ingredient = Ingredient.objects.filter(name__icontains=query)
        if ingredient.exists():
            recipe = get_object_or_404(Recipe , ingredient=ingredient)
            serializer = RecipeSerializer(recipe, many=True)
            return Response(serializer.data)
    


    


    

# Create your views here.
