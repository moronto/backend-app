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
        path('statistics/',statistiquesMovement,name='statistics'),
        path('detailsMovement/<int:id>',getMovement,name='detailMovement'),
        path('addSortie/',addSortie,name='addSortie'),
        path('infoMateriel/<str:ref>',infoMateriel,name='infoMateriel'),
        path('delete/<int:id>',deleteMovement,name='deleteMovement'),
        path('update/<int:id>',updateMovement,name='updateMovement'),
        path('retirerMateriel/',retirerMateriel,name='retirerMateriel'),
        #url chargeaffaire
        path('chargeaffaire/',chargeAffaire,name='chargeAffaire'),
        #url reservation
        path('reservation/',view=reservation,name='reservation'),
        path('newreservation/',view=newreservation,name='newReservation'),

]
