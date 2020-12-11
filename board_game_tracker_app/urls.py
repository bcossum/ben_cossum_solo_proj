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
    path('game/<int:game_id>', views.game_page),
    path('game/<str:game_title>', views.game),
    path('game/<int:game_id>/add_fav', views.add_fav),
    path('game/<int:game_id>/record_play', views.record_play),
    path('game/<int:game_id>/record_play/<int:play_id>', views.record_play_form),
    path('game_search', views.game_search),
    path('game_search/<str:term>', views.game_search_results),
    path('game/<int:game_id>/record_play/<int:play_id>/add_player', views.add_player),
    path('game/<int:game_id>/view_play/<int:play_id>/submit', views.submit_play),
]