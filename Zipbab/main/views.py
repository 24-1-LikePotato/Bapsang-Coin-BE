from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Fridge,FridgeIngredient,User
from .serializers import FridgeSerializer

class FridgeDetailView(APIView):
    
    def delete(self, request, user_id):
        fridge_ingredient_id = request.data.get('fridge_ingredient_id')

        if not fridge_ingredient_id:
            return Response({'message': 'fridge_ingredient_id가 제공되지 않았습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        # BODY로 받은 fridge_ingredient_id로 객체 찾기
        try:
            fridge_ingredient = FridgeIngredient.objects.get(pk=fridge_ingredient_id)
        
        except FridgeIngredient.DoesNotExist:
            return Response({'message': '해당 fridge_ingredient가 존재하지 않거나 유효하지 않습니다.'}, status=status.HTTP_404_NOT_FOUND)
        
        # Delete the fridge ingredient
        fridge_ingredient.delete()
        return Response({'message': '식재료가 정상적으로 삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)

        
