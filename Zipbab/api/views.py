from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from apscheduler.schedulers.background import BackgroundScheduler
import time
import os
import environ
import requests
from main.models import Ingredient
from price.models import ChangePriceDay
from main.serializers import RecipeSerializer, IngredientSerializer
from datetime import datetime
from django.conf import settings

# 환경변수를 불러올 수 있는 상태로 설정
env = environ.Env(DEBUG=(bool, True))

# 읽어올 환경 변수 파일을 지정
environ.Env.read_env(
  env_file=os.path.join(settings.BASE_DIR, '.env')
)

def job():
    print(f'******{time.strftime("%H:%M:%S")}******')

    # 식재료 api 호출해서 업데이트하는 코드
    serializer_class = IngredientSerializer
    ingredient_api_key = env('INGREDIENT_API_KEY')
    ingredient_api_id = env('INGREDIENT_API_ID')

    url = f'http://www.kamis.or.kr/service/price/xml.do?action=dailySalesList&p_cert_key={ingredient_api_key}&p_cert_id={ingredient_api_id}&p_returntype=json'
    response = requests.get(url)
    response.raise_for_status()  # Check if the request was successful
    price_list = response.json()['price']

    for i in price_list:
        product_name = i.get('productName')

        if not product_name:
            continue

        name, item = product_name.split(' ')

        if not Ingredient.objects.filter(name=name).exists():
            continue

        try:
            ingredient = Ingredient.objects.get(name=name, item = item)
        except Ingredient.DoesNotExist:
            continue

        try:
                change_price_day = ChangePriceDay.objects.get(ingredient=ingredient)
                change_price_day.date = datetime.today().strftime("%Y-%m-%d").date()
                change_price_day.price = i.get('price', "-")  # price 필드 수정
                change_price_day.updown = i.get('direction', "-")  # updown 필드 수정
                change_price_day.updown_percent = i.get('value', "-")  # updown_percent 필드 수정
                change_price_day.save()
        except ChangePriceDay.DoesNotExist:
                print("ChangePriceDay.DoesNotExist")

    print("************************")

def cron_prices():
    sched = BackgroundScheduler()
    # cron - 매일 아침 6시에 실행
    sched.add_job(job, 'cron', hour=6, minute=0, id='cron_weather')
    sched.start()

def index(request):
    return render(request, 'index.html')
