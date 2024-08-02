from apscheduler.schedulers.background import BackgroundScheduler
from main.models import Ingredient
from price.models import ChangePriceDay
from main.serializers import IngredientSerializer
import requests
import time
import datetime
from django.conf import settings
from django.db import connection

# 스케줄러가 이미 시작되었는지 확인하기 위한 전역 변수
scheduler_started = False

def job():
    print(f'******{time.strftime("%H:%M:%S")}******')

    # 식재료 API 호출해서 업데이트하는 코드
    ingredient_api_key = settings.INGREDIENT_API_KEY
    ingredient_api_id = settings.INGREDIENT_API_ID

    url = f'http://www.kamis.or.kr/service/price/xml.do?action=dailySalesList&p_cert_key={ingredient_api_key}&p_cert_id={ingredient_api_id}&p_returntype=json'
    response = requests.get(url)
    response.raise_for_status()  # Check if the request was successful
    price_list = response.json().get('price', [])

    for i in price_list:
        product_name = i.get('productName')

        if not product_name:
            continue

        name, item = product_name.split(' ')

        if not Ingredient.objects.filter(name=name).exists():
            continue

        try:
            ingredient = Ingredient.objects.get(name=name, item=item)
        except Ingredient.DoesNotExist:
            continue

        try:
            change_price_day = ChangePriceDay.objects.get(ingredient=ingredient)
            change_price_day.date = datetime.datetime.today().strftime("%Y-%m-%d").date()
            change_price_day.price = i.get('price', "-")  # price 필드 수정
            change_price_day.updown = i.get('direction', "-")  # updown 필드 수정
            change_price_day.updown_percent = i.get('value', "-")  # updown_percent 필드 수정
            change_price_day.save()
        except ChangePriceDay.DoesNotExist:
            print("ChangePriceDay.DoesNotExist")

    print("************************")

def cron_prices():
    global scheduler_started

    if not scheduler_started:
        sched = BackgroundScheduler()
        # cron - 매일 아침 6시에 실행
        sched.add_job(job, 'cron', hour=13, minute=50, id='cron_prices')
        sched.start()
        scheduler_started = True
