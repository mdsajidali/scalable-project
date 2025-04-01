from rest_framework import serializers
from .models import MealPlan, Meal

class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = ['id', 'meal_type', 'name', 'description', 'calories', 
                 'protein', 'carbs', 'fat', 'ingredients', 'preparation']
        read_only_fields = ['id']

class MealPlanSerializer(serializers.ModelSerializer):
    meals = MealSerializer(many=True, read_only=True)
    username = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = MealPlan
        fields = ['id', 'user', 'username', 'created_at', 'location', 
                 'temperature', 'weather_condition', 'calories_burned', 
                 'steps', 'meals']
        read_only_fields = ['id', 'user', 'username', 'created_at']