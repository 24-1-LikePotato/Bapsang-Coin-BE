from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Fridge,FridgeIngredient,User
from .serializers import FridgeSerializer

class FridgeDetailView(APIView):
    def get(self, request, user_id):

        # 등록된 유저가 없다면?
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({'message': '등록된 유저가 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
        
        # 등록된 냉장고가 없다면? : 이 경우는 없어야하는데 혹시 모르니깐
        try:
            fridge = Fridge.objects.get(user=user)
        except Fridge.DoesNotExist:
            return Response({'message': '등록된 냉장고가 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
        

        fridge = get_object_or_404(Fridge, user_id=user_id)
        fridge_ingredients = FridgeIngredient.objects.filter(fridge=fridge)

        if not fridge_ingredients.exists():
            return Response({'message': '등록한 식재료가 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = FridgeSerializer(fridge)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    

        
