from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Fridge,FridgeIngredient,User
from .serializers import FridgeSerializer,FridgeIngredientCreateSerializer

class FridgeDetailView(APIView):
    def get(self, request, user_id):

        # 등록된 유저가 없다면?
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({'message': '등록된 유저가 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
        
        fridge = get_object_or_404(Fridge, user_id=user_id)
        fridge_ingredients = FridgeIngredient.objects.filter(fridge=fridge)

        if not fridge_ingredients.exists():
            return Response({'message': '등록한 식재료가 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = FridgeSerializer(fridge)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    def post(self, request, user_id):
        
        # 등록된 유저가 없다면?
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({'message': '등록된 유저가 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
        
        fridge = get_object_or_404(Fridge, user=user)

        serializer = FridgeIngredientCreateSerializer(data=request.data, context={'fridge': fridge})
        
        if serializer.is_valid():
            serializer.save()
            return Response({'message': '정상적으로 식재료가 등록되었습니다.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)