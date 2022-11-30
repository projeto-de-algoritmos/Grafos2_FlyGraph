from django.urls import path
from . import views

urlpatterns = [
    path('get-data/', views.getData),
    path('airports/', views.getAirports),
    path('check-graph/', views.checkGraph),
    path('plot/', views.plot),
    path('plot-path/', views.plotPath)
]
