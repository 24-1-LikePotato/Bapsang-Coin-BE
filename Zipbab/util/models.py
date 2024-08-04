from django.db import models
from account.models import User
from main.models import FridgeIngredient


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    FridgeIngredient = models.ForeignKey(FridgeIngredient, on_delete=models.CASCADE)
    message = models.TextField()
    send_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)