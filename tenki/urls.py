from django.urls import path
from . import views

app_name    = "tenki"
urlpatterns = [
    path('', views.index, name="index"),
]
