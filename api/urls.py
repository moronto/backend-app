from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter

route=DefaultRouter()

route.register('stock',StockData,basename="stock"),
route.register('movements',movements,basename="movements"),

urlpatterns = [
    path("",include(route.urls)),
        path('stocks/<str:ref>/', detailStock, name='stock-detail'),
        path('stock/<str:ref>/', deleteStock, name='stock-delete'),
        path('stock/update/<str:ref>/', updateStock, name='update-delete'),
        path('stocks/', addStock, name='addStock'),
        #url movements

]
