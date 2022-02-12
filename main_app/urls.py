from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('user/<username>/', views.profile, name='profile'),
    path('character/create/', views.character_creation.as_view(), name='character_create'),
    path('characters/', views.character_index, name='character_index'),
    path('character/<int:character_id>/', views.character_show, name='character_show'),
    path('character/<int:pk>/update/', views.character_update.as_view(), name='character_update'),
    path('character/<int:pk>/delete/', views.character_delete.as_view(), name='character_delete'),
    path('weapon/create/', views.weapon_creation.as_view(), name='weapon_create'),
    path('weapons/', views.weapon_index, name='weapon_index'),
    path('weapon/<int:weapon_id>/', views.weapon_show, name='weapon_show'),
    path('weapon/<int:pk>/update/', views.weapon_update.as_view(), name='weapon_update'),
    path('weapon/<int:pk>/delete/', views.weapon_delete.as_view(), name='weapon_delete'),
    # path('room/create/', views.room_create.as_view(), name='room_create'),
    path('room/<str:room_name>/<username>/<int:character_id>/', views.room_show, name='room_show'),
    path('room/search/<username>/', views.room_search, name='room_search')
]
