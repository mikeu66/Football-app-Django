from django.urls import path
from . import views

urlpatterns = [
    path('myview/', views.myview),
    path("search/", views.searchView),
    path("search/<player_name>", views.myview),
    path("allPlayers", views.allPlayersView),
    path("pull/<player_name>", views.pullPlayerStats)
]