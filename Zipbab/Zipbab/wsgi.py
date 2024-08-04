"""
WSGI config for BapsangCoin project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Zipbab.settings')

application = get_wsgi_application()

# 스케줄러 시작
try:
    from api.views import cron_prices, scheduler_started
    if not scheduler_started:
        cron_prices()
        scheduler_started = True
except Exception as e:
    print(f"Error starting scheduler: {e}")
