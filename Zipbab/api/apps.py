from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
    def ready(self):
        from main.models import Ingredient
        from price.models import ChangePriceDay
        from main.serializers import RecipeSerializer, IngredientSerializer
        from .views import cron_prices
        cron_prices()
