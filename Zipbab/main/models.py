from django.db import models
from account.models import User
from datetime import datetime

class Fridge(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.user.nickname}의 냉장고"

class Ingredient(models.Model):
    name = models.CharField(max_length=50,verbose_name='품종', default='NONE')
    item = models.CharField(max_length=50,verbose_name='품목', default='NONE')
    code = models.CharField(max_length=50,verbose_name='식품코드', default='0')
    unit = models.CharField(max_length=50,verbose_name='단위',default='0')

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

    def days_until_expiration(self):
        today = datetime.now().date()
        delta = self.expiration_date - today
        return delta.days

    def is_expiring_soon(self, threshold=1):
        return self.days_until_expiration() <= threshold

class Recipe(models.Model):
    name = models.CharField(max_length=30) # 메뉴명
    content = models.TextField() # 만드는 법
    ingredient_list = models.TextField()  # 기존 ingredient 필드명 변경
    image = models.URLField(max_length=200, blank = True, null=True)  # ImageField에서 URLField로 변경
    calorie = models.FloatField() # 열량
    carb = models.FloatField() # 탄수화물
    protein = models.FloatField() # 단백질
    fat = models.FloatField() # 지방
    natrium = models.FloatField() # 나트륨

    def __str__(self) -> str:
        return self.name
    

class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(Ingredient,on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.recipe.name}의 {self.ingredient.name}"