from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MealPlanViewSet, MealAPIView, PublicMealPlanAPI
from . import views

# Create a router and register our viewsets
router = DefaultRouter()
router.register(r'meal-plans', MealPlanViewSet, basename='meal-plan')

urlpatterns = [
    path('', include(router.urls)),
    path('meal-plans/<int:meal_plan_id>/meals/', MealAPIView.as_view(), name='meals-list'),
    path('meal-plans/<int:meal_plan_id>/meals/<int:meal_id>/', MealAPIView.as_view(), name='meal-detail'),
    # Public API endpoint for other applications
    path('public/users/<int:user_id>/meal-plans/<int:meal_plan_id>/', PublicMealPlanAPI.as_view(), name='public-meal-plan'),
    #path('test/', views.test_api, name='test-api'),
]