from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    user_id = models.CharField(max_length=10, unique=True, primary_key=True)
    name = models.CharField(max_length=10)
    email = models.EmailField()
    password = models.CharField(max_length=20)
    nickname = models.CharField(max_length=10,unique=True)
    subscription = models.BooleanField(default=False)

class Fridge(models.Model):
    fridge_id  = models.AutoField(unique=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)


class FridgeIngredient(models.Model):
    fridge_id = models.ForeignKey(Fridge, on_delete=models.CASCADE)
    ingredient_id = models.IntegerField(unique=True)


class Ingredient(models.Model):
    name = models.CharField(max_length = 20)


class Recipe(models.Model):
    Ingredient_id = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    rcp_name = models.CharField(max_length=30)
    content = models.TextField()
    ingredient = models.TextField()
    image = models.ImageField(upload_to='images/')
    calorie = models.IntegerField()
    carb = models.IntegerField()
    protein = models.IntegerField()
    fat = models.IntegerField()
    natrium = models.IntegerField()

class Notification(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    fridge_id = models.ForeignKey(Fridge,on_delete=models.CASCADE)
    message = models.TextField()
    send_at = models.DateTimeField(auto_now_add=True)
    create_at = models.DateTimeField(auto_now_add=True)

class ChangePriceMonth(models.Model):
    ingredient_id = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    month = models.IntegerField()
    average_price = models.IntegerField()
    updown = models.IntegerField(choices=[(0,1,2)])
    updown_percent = models.IntegerField()
    max = models.IntegerField()
    min = models.IntegerField()

class ChangePriceDay(models.Model):
    ingredient_id = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    month = models.IntegerField()
    average_price = models.IntegerField()
    updown = models.IntegerField(choices=[(0,1,2)])
    updown_percent = models.IntegerField()
    max = models.IntegerField()
    min = models.IntegerField()

