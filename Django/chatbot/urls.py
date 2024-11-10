"""
URL configuration for chatbot project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from chatbot_app import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('chat/', views.chat_bot, name='chat_bot'),
    path('api/saldo/<str:numero_cuenta>/', views.consultar_saldo, name='consultar_saldo'),
    path('api/estado-cuenta/<str:numero_cuenta>/', views.consultar_estado_cuenta, name='consultar_estado_cuenta'),
    path('api/convertir/', views.convertir_moneda, name='convertir_moneda'),
    path('api/expenses/', views.create_expense, name='create_expense'),
    path('api/budget/', views.check_budget, name='check_budget'),
] 

