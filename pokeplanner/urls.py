from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("add_goals",views.add_goals,name="add_goals"),
    path("add_purchase",views.add_purchase,name="add_purchase"),
    path("login", views.login_view, name="login"),
    path("register", views.register, name="register"),
    path("new_user", views.new_user, name="new_user"),
    path("logout", views.logout_view, name="logout"),
]