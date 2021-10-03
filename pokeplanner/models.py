from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE

import datetime

# Create your models here.

CATEGORIES = [("Rent", "Rent"),("Bills", "Bills"),("Taxes", "Taxes"),("Food", "Food"), ("Transportation", "Transportation"), ("Entertainment", "Entertainment"), ("Miscellaenous","Miscellaenous")]

class Week(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE, related_name="weeks",blank=True,null=True)
    week = models.IntegerField(blank=True)
    year = models.IntegerField(blank=True)

class Goal(models.Model):
    max_value = models.DecimalField(max_digits=10,decimal_places=2)
    balance = models.DecimalField(max_digits=10,decimal_places=2, default=0)
    isMaxed = balance > max_value
    category = models.CharField(max_length=64, blank=True)
    week = models.ForeignKey(Week, on_delete=CASCADE, related_name="goals")

class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE, related_name="purchases",blank=True,null=True)
    name = models.CharField(max_length=64)
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    goal = models.ForeignKey(Goal, on_delete=CASCADE, related_name="purchases")

class Pokemon(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE, related_name="pokemon",blank=True,null=True)
    nickname = models.CharField(max_length=64)
    name = models.CharField(max_length=64, blank=True, choices=[("squirtle", "Squirtle")])
    xp = models.IntegerField(default=0)
    level = models.IntegerField(default=0)