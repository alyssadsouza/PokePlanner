from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Week, Purchase, Pokemon, Goal

import datetime

 # Create your views here.

end_of_week = (datetime.datetime.today().weekday() == 6)

@login_required(login_url="login")
def index(request):

    global end_of_week

    try:
        this_week = Week.objects.get(user=request.user,week=datetime.datetime.today().isocalendar()[1], year=datetime.datetime.today().isocalendar()[0])
        goals = Goal.objects.filter(week=this_week)
        goals_set = True
    except:
        goals_set = False
        goals = ["Rent","Bills","Taxes","Food","Transportation","Entertainment","Miscellaenous"]

    if end_of_week and goals_set:
        saved = [goal for goal in goals if goal.isMaxed]
        xp = len(saved)*100
        pokemon = Pokemon.objects.get(user=request.user)
        pokemon.xp += xp
        pokemon.save()

        if pokemon.xp > 1000:
            pokemon.level += 1
            pokemon.xp -= 1000
            pokemon.save()

        end_of_week = False
    else:
        saved = []
        xp = 0

    if request.method == "POST":

        income = request.POST["income"]
        # calculate goal values for different categories in empty list below
        goal_values = [10,20,30,40,30,20,10]
        goal_values = zip(goals,goal_values)

        return render(request, "index.html",{
            "pokemon": Pokemon.objects.get(user=request.user),
            "goals_set": goals_set,
            "goals": goals,
            "income": True,
            "goal_values": goal_values,
            "end_of_week": end_of_week,
            "saved":saved,
            "xp":xp

        })

    return render(request, "index.html",{
        "pokemon": Pokemon.objects.get(user=request.user),
        "goals_set": goals_set,
        "goals": goals,
        "income": False,
        "goal_values": [],
        "end_of_week": end_of_week,
        "saved":saved,
        "xp":xp
    })

def add_goals(request):
    if request.method == "POST":
        week = Week(user=request.user,week=datetime.datetime.today().isocalendar()[1], year=datetime.datetime.today().isocalendar()[0])
        week.save()
        rent = Goal(max_value=request.POST["Rent"], category="Rent",week=week)
        bills = Goal(max_value=request.POST["Bills"], category="Bills",week=week)
        taxes = Goal(max_value=request.POST["Taxes"], category="Taxes",week=week)
        food = Goal(max_value=request.POST["Food"], category="Food",week=week)
        entertainment = Goal(max_value=request.POST["Entertainment"], category="Entertainment",week=week)
        transport = Goal(max_value=request.POST["Transportation"], category="Transportation",week=week)
        misc = Goal(max_value=request.POST["Miscellaenous"], category="Miscellaenous",week=week)
        rent.save()
        bills.save()
        taxes.save()
        food.save()
        entertainment.save()
        transport.save()
        misc.save()

    return redirect("index")

def add_purchase(request):
    if request.method == "POST":
        name = request.POST["name"]
        category = request.POST["category"]
        amount = request.POST["amount"]
        week = Week.objects.get(user=request.user,week=datetime.datetime.today().isocalendar()[1], year=datetime.datetime.today().isocalendar()[0])
        goal = Goal.objects.get(week=week,category=category)

        purchase = Purchase(user=request.user,name=name,amount=amount,goal=goal)
        purchase.save()

        goal.balance += int(amount)
        goal.save()

    return redirect("index")

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            return render(request, "login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "login.html")

@login_required
def logout_view(request):
    logout(request)
    return redirect("index")


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return redirect("new_user")
    else:
        return render(request, "register.html")

def new_user(request):
    if request.method == "POST":

        if len(request.POST["nickname"]) == 0:
            nickname = request.POST["name"]
        else:
            nickname = request.POST["nickname"]

        pokemon = Pokemon(user = request.user, nickname = nickname, name = request.POST["name"])
        pokemon.save()
        return redirect("index")

    return render(request, "new_user.html")