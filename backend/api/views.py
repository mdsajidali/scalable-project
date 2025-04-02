from rest_framework import viewsets, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import MealPlan, Meal
from .serializers import MealPlanSerializer, MealSerializer
from .tasks import generate_meal_plan_task
from .services import get_weather_data, get_fitness_data, generate_meal_plan

class MealPlanViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing meal plans
    """
    serializer_class = MealPlanSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        This view returns meal plans for the currently authenticated user
        """
        user = self.request.user
        return MealPlan.objects.filter(user=user).order_by('-created_at')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['post'])
    def generate(self, request):
        """
        Generate a new meal plan based on user location and fitness data
        """
        location = request.data.get('location')
        if not location:
            return Response(
                {'error': 'Location is required to generate a meal plan'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if manual fitness data was provided
        manual_fitness_data = request.data.get('manual_fitness_data')
        
        # Run synchronously instead of as a Celery task
        result = generate_meal_plan_task(
            request.user.id, 
            location,
            manual_fitness_data=manual_fitness_data
        )
        
        if not result:
            return Response({
                'error': 'Failed to generate meal plan'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        meal_plan_id = result.get('meal_plan_id')
        warnings = result.get('warnings', [])
        
        if meal_plan_id:
            return Response({
                'message': 'Meal plan generated successfully',
                'meal_plan_id': meal_plan_id,
                'warnings': warnings
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'error': 'Failed to generate meal plan',
                'warnings': warnings
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def latest(self, request):
        """
        Get the latest meal plan for the current user
        """
        try:
            meal_plan = MealPlan.objects.filter(user=request.user).latest('created_at')
            serializer = self.get_serializer(meal_plan)
            return Response(serializer.data)
        except MealPlan.DoesNotExist:
            return Response({
                'message': 'No meal plans found for this user'
            }, status=status.HTTP_404_NOT_FOUND)

class MealAPIView(APIView):
    """
    API View for Meal objects
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, meal_plan_id, meal_id=None):
        # Check if the meal plan belongs to the current user
        meal_plan = get_object_or_404(MealPlan, id=meal_plan_id, user=request.user)
        
        if meal_id:
            # Get a specific meal
            meal = get_object_or_404(Meal, id=meal_id, meal_plan=meal_plan)
            serializer = MealSerializer(meal)
            return Response(serializer.data)
        else:
            # Get all meals for the meal plan
            meals = Meal.objects.filter(meal_plan=meal_plan)
            serializer = MealSerializer(meals, many=True)
            return Response(serializer.data)

# Public API for other applications to access meal plans
class PublicMealPlanAPI(generics.RetrieveAPIView):
    """
    Public API endpoint for accessing meal plans by other applications
    """
    serializer_class = MealPlanSerializer
    
    def get_object(self):
        """
        Return a meal plan based on user_id and meal_plan_id
        """
        user_id = self.kwargs.get('user_id')
        meal_plan_id = self.kwargs.get('meal_plan_id')
        
        return get_object_or_404(MealPlan, id=meal_plan_id, user__id=user_id)