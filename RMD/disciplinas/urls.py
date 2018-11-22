from django.contrib import admin
from django.urls import path
from .views import disciplina

urlpatterns = [
    path('<str:disciplina>/', disciplina, name="disciplina")
]