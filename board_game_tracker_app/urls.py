from django.urls import path
from . import views

urlpatterns = [
    path('', views.reg),
    path('login', views.login),
    path('reg', views.reg),
    path('home', views.home),
    path('logout', views.logout),
    path('add_game', views.add_game),
    path('user/<int:user_id>', views.profile),
    path('user/<int:user_id>/edit', views.edit_profile),
    path('user/<int:user_id>/edit_profile', views.edit_profile),
    path('game/<str:game_title>', views.game),
    path('game/<str:game_title>/add_fav', views.add_fav),
    path('game/<str:game_title>/record_play', views.record_play)
]