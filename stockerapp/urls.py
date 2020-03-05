from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('stockinfo/<str:ticker>/', views.stockinfo, name='stockinfo'),
    path('stockdaily/<str:ticker>/', views.stockdaily, name='stockdaily'),
]
