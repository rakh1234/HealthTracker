from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views, api_views

# Create a router for API viewsets
router = DefaultRouter()
router.register(r'activities', api_views.ActivityViewSet)
router.register(r'nutrition', api_views.NutritionEntryViewSet)
router.register(r'goals', api_views.UserGoalViewSet)

urlpatterns = [
    # Traditional Django views (for backward compatibility)
    path('', views.home, name='home'),
    # path('register/', views.register, name='register'),
    # path('login/', views.user_login, name='login'),
    # path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('goals/', views.goal_settings, name='goal_settings'),
    path('activities/', views.activity_list, name='activity_list'),
    path(
        'activities/create/',
        views.activity_create,
        name='activity_create'
    ),
    path(
        'activities/<int:pk>/update/',
        views.activity_update,
        name='activity_update'
    ),
    path(
        'activities/<int:pk>/delete/',
        views.activity_delete,
        name='activity_delete'
    ),
    path('nutrition/', views.nutrition_list, name='nutrition_list'),
    path(
        'nutrition/create/',
        views.nutrition_create,
        name='nutrition_create'
    ),
    path(
        'nutrition/<int:pk>/update/',
        views.nutrition_update,
        name='nutrition_update'
    ),
    path(
        'nutrition/<int:pk>/delete/',
        views.nutrition_delete,
        name='nutrition_delete'
    ),

    # REST API endpoints
    path('api/', include(router.urls)),
    path(
        'api/dashboard/',
        api_views.dashboard_stats,
        name='api_dashboard_stats'
    ),
]
