
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from home import urls as home_urls
from disciplinas import urls as disciplinas_urls


urlpatterns = [
    path('', include(home_urls)),
    path('disciplinas/', include(disciplinas_urls)),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('admin/', admin.site.urls)
]   