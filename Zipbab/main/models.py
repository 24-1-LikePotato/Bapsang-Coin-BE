from django.db import models
from account.models import User

class Fridge(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.user.nickname}의 냉장고"

class Ingredient(models.Model):
    name = models.CharField(max_length=50,verbose_name='품종', default='NONE')
    item = models.CharField(max_length=50,verbose_name='품목', default='NONE')
    code = models.CharField(max_length=50,verbose_name='식품코드', default='0')

    def __str__(self) -> str:
        return self.name

class FridgeIngredient(models.Model):
    fridge = models.ForeignKey(Fridge, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateField()
    purchase_date = models.DateField()

    def __str__(self) -> str:
        return f"{self.fridge.user.nickname}의 냉장고 - {self.ingredient.name}"


class Recipe(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    content = models.TextField()
    ingredient_list = models.TextField()  # 기존 ingredient 필드명 변경
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    calorie = models.FloatField()
    carb = models.FloatField()
    protein = models.FloatField()
    fat = models.FloatField()
    natrium = models.FloatField()

    def __str__(self) -> str:
        return f"[ {self.ingredient.name} ] : {self.name}"