from django.urls import path

from . import views

app_name = 'stockerapp'
urlpatterns = [
    path('', views.index, name='index'),
    path('stockinfo/<str:ticker>/', views.stockinfo, name='stockinfo'),
    path('stockdaily/<str:ticker>/', views.stockdaily, name='stockdaily'),
    path('portfolio/<int:portfolio_id>/', views.portfolio, name='portfolio'),
    path('new_order/<int:portfolio_id>/', views.new_order, name='new_order'),
    path('new_ticker/', views.new_ticker, name='new_ticker'),
]
