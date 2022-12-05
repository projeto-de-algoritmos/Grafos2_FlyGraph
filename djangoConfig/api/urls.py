from django.urls import path
from . import views

urlpatterns = [
    path('get-data/', views.getData),
    path('get-data-dijkstra/', views.getDataDijkstra),
    path('get-data-multi-bfs/', views.getDataMultiBfs),
    path('airports/', views.getAirports),
    path('check-graph/', views.checkGraph),
    path('plot/', views.plot),
    path('plot-path/', views.plotPath)
]
