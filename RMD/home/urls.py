from django.urls import path
from .views import home, logout_view, submeter_arquivos

urlpatterns = [
    path('', home, name='home'),
    path('logout/', logout_view, name='logout'),
    path('submeter/', submeter_arquivos, name='submeter_arquivos')
]