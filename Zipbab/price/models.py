from django.db import models
from main.models import Ingredient

class ChangePriceMonth(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    month = models.CharField(max_length=7)  # 'YYYY-MM' 형식
    average_price = models.IntegerField()
    updown = models.IntegerField(choices=[
        (0, 'Up'),
        (1, 'Down'),
        (2, 'Same')
    ])
    updown_percent = models.FloatField()

    def __str__(self) -> str:
        return f"[ {self.ingredient.name} ] : {self.month}월 가격"

class ChangePriceDay(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    date = models.DateField()  # 일 단위로 저장
    price = models.IntegerField()
    updown = models.IntegerField(choices=[
        (0, 'Up'),
        (1, 'Down'),
        (2, 'Same')
    ])
    updown_percent = models.FloatField()


    def __str__(self) -> str:
        return f"[ {self.ingredient.name} ] : {self.date}월 가격"
