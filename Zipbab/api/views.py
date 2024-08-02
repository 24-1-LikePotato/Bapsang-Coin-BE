from apscheduler.schedulers.background import BackgroundScheduler
from main.models import Ingredient
from price.models import ChangePriceDay
from main.serializers import IngredientSerializer
import requests
import time
import datetime
import os
import environ
from django.conf import settings
from django.db import connection

# 스케줄러가 이미 시작되었는지 확인하기 위한 전역 변수
scheduler_started = False

env = environ.Env(DEBUG=(bool, True))

environ.Env.read_env(
  env_file=os.path.join(settings.BASE_DIR, '.env')
)

def validate_price(price):
    try:
        # 쉼표가 포함된 숫자 문자열을 처리
        if isinstance(price, str):
            price = price.replace(',', '')
        return int(price)
    except (ValueError, TypeError):
        return -1

def job():
    print(f'******{time.strftime("%H:%M:%S")}******')

    # 식재료 API 호출해서 업데이트하는 코드
    ingredient_api_key = env('INGREDIENT_API_KEY')
    ingredient_api_id = env('INGREDIENT_API_ID')

    url = f'http://www.kamis.or.kr/service/price/xml.do?action=dailySalesList&p_cert_key={ingredient_api_key}&p_cert_id={ingredient_api_id}&p_returntype=json'
    response = requests.get(url)
    response.raise_for_status()  # Check if the request was successful
    recent_date = response.json().get('condition')[0][0]
    price_list = response.json().get('price', [])

    for i in price_list:
        product_name = i.get('productName')

        if not product_name:
            continue

        name, item = product_name.split('/')

        if not Ingredient.objects.filter(name=name).exists():
            continue

        try:
            ingredient = Ingredient.objects.get(name=name, item=item)
        except Ingredient.DoesNotExist:
            continue

        try:
            change_price_day = ChangePriceDay.objects.get(ingredient=ingredient)
            today_date = datetime.datetime.strptime(recent_date, "%Y-%m-%d").date()
            change_price_day.date = today_date
            change_price_day.price = validate_price(i.get('dpr1', "-1"))
            change_price_day.updown = i.get('direction', "-1")  # updown 필드 수정
            change_price_day.updown_percent = i.get('value', "-1")  # updown_percent 필드 수정
            print(f"{product_name} : {change_price_day.price}원 | {change_price_day.updown} | {change_price_day.updown_percent}%")
            change_price_day.save()
        except ChangePriceDay.DoesNotExist:
            print("ChangePriceDay.DoesNotExist")

    print("************************")

def cron_prices():
    global scheduler_started

    if not scheduler_started:
        sched = BackgroundScheduler(timezone='Asia/Seoul')
        # cron - 매일 아침 6시에 실행
        sched.add_job(job, 'cron', hour=15, minute=12, id='cron_prices')
        sched.start()
        scheduler_started = True
