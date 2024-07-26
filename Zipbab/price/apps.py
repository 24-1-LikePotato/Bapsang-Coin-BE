from django.apps import AppConfig
import os

class PriceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'price'

    def ready(self):
        from .utils import load_ingredients_from_csv
        from .models import Ingredient
        from django.conf import settings

        if not Ingredient.objects.exists():
            file_path = settings.CSV_FILE_PATH
            load_ingredients_from_csv(file_path)
