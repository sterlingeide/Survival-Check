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
]
