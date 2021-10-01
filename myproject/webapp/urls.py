from django.urls import path
from . import views

urlpatterns = [
	path('', views.apiOverview, name="api-overview"),
	path('leagues/', views.leagueslist, name="leagues-list"),
	path('leagues/<str:pk>/', views.leaguesdetail, name="leagues-detail"),
    path('leagues/<str:pk>/teams/', views.leaguesdetailteam, name="leagues-detail-teams"),
    path('leagues/<str:pk>/teams/train/', views.ligatrain, name="leagues-train"),
    path('leagues/<str:pk>/players/', views.leaguesplayers, name="leagues-detail-teams"),
    path('teams/', views.teamlist, name="team-list"),
	path('teams/<str:pk>/', views.teamsdetail, name="teams-detail"),
    path('teams/<str:pk>/players/', views.teamsdetailplayer, name="teams-detail-player"),
    path('teams/<str:pk>/players/train/', views.teamtrain, name="teams-train"),
    path('players/', views.playerlist, name="players-list"),
	path('players/<str:pk>/', views.playerdetail, name="players-detail"),
    path('players/<str:pk>/train/', views.playertrain, name="players-train"),
]
