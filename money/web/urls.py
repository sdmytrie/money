from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.money_login, name="login"),
    path("create-banks/", views.create_banks, name="create-banks")
]
