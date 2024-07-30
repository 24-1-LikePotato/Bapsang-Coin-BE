from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Fridge,FridgeIngredient,User,Recipe,Ingredient, RecipeIngredient
from .serializers import FridgeSerializer,RecipeSerializer

import os
import environ
import requests
from django.conf import settings

from .models import Fridge,FridgeIngredient,User
from .serializers import FridgeIngredientCreateSerializer

class FridgeDetailView(APIView):
    def post(self, request, user_id):
        
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
    
    


# 환경변수를 불러올 수 있는 상태로 설정
env = environ.Env(DEBUG=(bool, True))

# 읽어올 환경 변수 파일을 지정
environ.Env.read_env(
  env_file=os.path.join(settings.BASE_DIR, '.env')
)

class RecipeStoreView(APIView):
    serializer_class = RecipeSerializer
    recipe_api_key = env('RECIPE_API_KEY')

    def post(self, request):
        url = f'http://openapi.foodsafetykorea.go.kr/api/{self.recipe_api_key}/COOKRCP01/json/{request.data.get('start_index')}/{request.data.get('end_index')}'
        
        try:
            response = requests.get(url)
            response.raise_for_status()  # Check if the request was successful
            recipe_list = response.json()['COOKRCP01']['row']  # 레시피 관련 부분만 가지고 옴
            
            for i in recipe_list: 
                # 만드는 법을 모두 불러와서 하나의 문자열로 만듦
                manual_list = []
                for j in range(1, 21):
                    key = f"MANUAL{j:02}"
                    if key in i and i[key]:
                        manual_list.append(i[key])
                    else:
                        break
                manual = '+'.join(manual_list)

                # 모델에 저장
                Recipe(
                    name=i.get('RCP_NM', ''), # 메뉴명
                    content=manual, # 만드는 법
                    ingredient_list=i.get('RCP_PARTS_DTLS', ''),  # 재료정보
                    image=i.get('ATT_FILE_NO_MAIN', ''), # 이미지
                    calorie=i.get('INFO_ENG', '-1'), # 열량
                    carb=i.get('INFO_CAR', '-1'), # 탄수화물
                    protein=i.get('INFO_PRO', '-1'), # 단백질
                    fat=i.get('INFO_FAT', '-1'), # 지방
                    natrium=i.get('INFO_NA', '-1') # 나트륨
                ).save()

        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"status": "success"}, status=status.HTTP_200_OK)


class RecipeIngredientStoreView(APIView):
    def post(self, request):
        recipes = Recipe.objects.all()
        for recipe in recipes:
            ingredient_list = recipe.ingredient_list
            ingredients = [ingredient.strip() for ingredient in ingredient_list.split(',')]

            # Clear existing RecipeIngredient relations for the current recipe
            RecipeIngredient.objects.filter(recipe=recipe).delete()

            # Create new RecipeIngredient relations for the current recipe
            for ingredient_entry in ingredients:
                ingredient_name = ingredient_entry.split(' ')[0]
                ingredient = Ingredient.objects.filter(name__icontains=ingredient_name).first()
                if ingredient:
                    RecipeIngredient.objects.create(recipe=recipe, ingredient=ingredient)

        return Response({"message": "All recipe ingredients updated successfully."}, status=status.HTTP_200_OK)



        fridge = get_object_or_404(Fridge, user=user)

        serializer = FridgeIngredientCreateSerializer(data=request.data, context={'fridge': fridge})
        
        if serializer.is_valid():
            serializer.save()
            return Response({'message': '정상적으로 식재료가 등록되었습니다.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)