from django.db import models
from main.models import Ingredient

class ChangePriceMonth1(models.Model): # 7번 api 맞게 수정 필요 (그래프에 사용)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    forty = models.IntegerField()
    thirty = models.IntegerField()
    twenty = models.IntegerField()
    ten = models.IntegerField()
    today = models.IntegerField()
    def __str__(self) -> str:
        return f"[ {self.ingredient.name} ] : {self.month}월 가격"

class ChangePriceDay(models.Model): # 6번 api
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    date = models.DateField()  # 일 단위로 저장 (day1)
    price = models.IntegerField() # 가격 (dpr1)
    updown = models.IntegerField(choices=[ # 등락 여부 (direction)
        (0, 'Up'),
        (1, 'Down'),
        (2, 'Same')
    ])
    updown_percent = models.FloatField() # 등락율 (value)


    def __str__(self) -> str:
        return f"[ {self.ingredient.name} ] : {self.date}월 가격"


class ChangePriceMonth2(models.Model): # 7번 api 맞게 수정 필요 (그래프에 사용)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    forty = models.IntegerField()
    thirty = models.IntegerField()
    twenty = models.IntegerField()
    ten = models.IntegerField()
    today = models.IntegerField()
    def __str__(self) -> str:
        return f"[ {self.ingredient.name} ] : {self.month}월 가격"