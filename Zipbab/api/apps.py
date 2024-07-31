from django.apps import AppConfig
import threading

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    # def ready(self):
    #     from .views import cron_prices, scheduler_started

    #     # 스케줄러가 이미 시작되지 않았는지 확인합니다.
    #     if not scheduler_started:
    #         scheduler_thread = threading.Thread(target=cron_prices)
    #         scheduler_thread.start()
    #         scheduler_started = True
