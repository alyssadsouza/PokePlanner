from django.db import models
from django.contrib.auth.models import User

from django.db.models.deletion import CASCADE

# Create your models here.

class Week(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE, related_name="weeks",blank=True,null=True)
    date = models.DateField(auto_now=True)

class Category(models.Model):
    CATEGORIES = [("rent", "Rent"),("bills", "Bills"),("taxes", "Taxes"),("food", "Food"), ("transport", "Transportation"), ("entertainment", "Entertainment"), ("misc","Miscellaenous")]
    category = models.CharField(max_length=64, blank=True, choices=CATEGORIES)

class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE, related_name="purchases",blank=True,null=True)
    name = models.CharField(max_length=64)
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    category = models.ForeignKey(Category, on_delete=CASCADE, related_name="purchases")
    week = models.ForeignKey(Week, on_delete=CASCADE, related_name="purchases")

class Goal(models.Model):
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    isMaxed = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=CASCADE, related_name="goals")
    week = models.ForeignKey(Week, on_delete=CASCADE, related_name="goals")

class Pokemon(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE, related_name="pokemon",blank=True,null=True)
    nickname = models.CharField(max_length=64)
    name = models.CharField(max_length=64, blank=True, choices=[("squirtle", "Squirtle")])
    xp = models.IntegerField(default=0)
    level = models.IntegerField(default=0)