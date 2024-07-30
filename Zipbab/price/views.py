import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ChangePriceDay
from .serializers import ChangePriceDaySerializer, TodayIngredient
from main.models import Ingredient
from main.serializers import IngredientSerializer
from datetime import datetime
import os
import environ
from django.conf import settings

# 환경변수를 불러올 수 있는 상태로 설정
env = environ.Env(DEBUG=(bool, True))
environ.Env.read_env(env_file=os.path.join(settings.BASE_DIR, '.env'))

class UpdateIngredientPriceView(APIView):
    serializer_class = IngredientSerializer
    ingredient_api_key = env('INGREDIENT_API_KEY')
    ingredient_api_id = env('INGREDIENT_API_ID')

    def post(self, request):
        # API 호출
        url = f'http://www.kamis.or.kr/service/price/xml.do?action=dailySalesList&p_cert_key={self.ingredient_api_key}&p_cert_id={self.ingredient_api_id}&p_returntype=json'
        response = requests.get(url)
        response.raise_for_status()
        price_list = response.json()['price']

        processed_names = set()  # 이미 처리된 name을 추적하는 세트

        for i in price_list:
            product_name = i.get('productName')

            if not product_name:
                continue

            try:
                name, item = product_name.split('/')
            except ValueError:
                continue

            if name in processed_names:
                continue  # 이미 처리된 name이면 건너뜀

            ingredient, created = Ingredient.objects.get_or_create(name=name)
            if not created:
                continue  # 이미 존재하는 name이면 건너뜀

            ingredient.item = item  # item 필드 업데이트
            ingredient.code = i.get('productno', ingredient.code)
            ingredient.save()

            # name을 처리된 세트에 추가
            processed_names.add(name)

            # Update or create ChangePriceDay
            date_str = i.get('day1')
            if date_str == "당일":
                date = datetime.today().date()
            else:
                try:
                    date = datetime.strptime(date_str, '%Y-%m-%d').date()  # 문자열을 date 객체로 변환
                except (ValueError, TypeError):
                    print(f"Skipping due to invalid date format: {date_str}")  # 디버깅 로그
                    continue

            try:
                price = int(i.get('dpr1', '0').replace(',', ''))
                direction = int(i.get('direction', '2'))  # Default to 'Same'
                value = float(i.get('value', '0.0'))
            except ValueError:
                print(f"Skipping due to invalid numeric values: {i}")  # 디버깅 로그
                continue  # 변환에 실패하면 건너뜀

            print(f"Processing {name} for date {date}")  # 디버깅 로그

            change_price_day, created = ChangePriceDay.objects.get_or_create(
                ingredient=ingredient,
                date=date,
                defaults={
                    'price': price,
                    'updown': direction,
                    'updown_percent': value
                }
            )

            if not created:
                change_price_day.price = price
                change_price_day.updown = direction
                change_price_day.updown_percent = value
                change_price_day.save()

            print(f"ChangePriceDay saved: {change_price_day}")  # 디버깅 로그

        return Response({"status": "success"}, status=status.HTTP_200_OK)


class TodayPriceView(APIView):
    def get(self, request):
        # 전체 ChangePriceDay 객체를 읽음
        change_price_days = ChangePriceDay.objects.all()
        
        if not change_price_days.exists():
            return Response({"error": "No data available"}, status=status.HTTP_404_NOT_FOUND)
        
        # 가격이 오른 것 중에 등락율이 제일 높은 것
        highest_up_item = change_price_days.filter(updown=0).order_by('-updown_percent').first()
        # 가격이 내려간 것 중에 등락율이 제일 낮은 것
        lowest_down_item = change_price_days.filter(updown=1).order_by('-updown_percent').first()
        
        highest_price_data = TodayIngredient(highest_up_item).data
        lowest_price_data = TodayIngredient(lowest_down_item).data
        
        return Response({
            "highest_price_item": highest_price_data,
            "lowest_price_item": lowest_price_data
        }, status=status.HTTP_200_OK)