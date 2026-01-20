from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('analytics/', views.analytics_dashboard, name='analytics_dashboard'),
    path('goals/', views.goal_settings, name='goal_settings'),
    path('activities/', views.activity_list, name='activity_list'),
    path('activities/create/', views.activity_create, name='activity_create'),
    path('activities/<int:pk>/update/', views.activity_update, name='activity_update'),
    path('activities/<int:pk>/delete/', views.activity_delete, name='activity_delete'),
    path('nutrition/', views.nutrition_list, name='nutrition_list'),
    path('nutrition/create/', views.nutrition_create, name='nutrition_create'),
    path('nutrition/<int:pk>/update/', views.nutrition_update, name='nutrition_update'),
    path('nutrition/<int:pk>/delete/', views.nutrition_delete, name='nutrition_delete'),
]