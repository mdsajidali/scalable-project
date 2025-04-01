from celery import shared_task
from .models import MealPlan, Meal
from .services import get_weather_data, get_fitness_data, generate_meal_plan
from django.contrib.auth.models import User

@shared_task
def generate_meal_plan_task(user_id, location):
    """
    Synchronous version of meal plan generation (with Celery task handling).
    """
    try:
        user = User.objects.get(id=user_id)
        user_profile = user.profile
        
        # Get weather data
        weather_data = get_weather_data(location)
        
        # Get fitness data
        fitness_data = get_fitness_data(user_id, user_profile.fitness_api_id)
        
        # Generate meal plan
        meal_plan_data = generate_meal_plan(user_profile, weather_data, fitness_data)
        
        # Create MealPlan record
        meal_plan = MealPlan.objects.create(
            user=user,
            location=location,
            temperature=weather_data.get('temperature', 20),
            weather_condition=weather_data.get('weather_condition', 'Unknown'),
            calories_burned=fitness_data.get('calories_burned', 0),
            steps=fitness_data.get('steps', 0)
        )
        
        # Create Meal records
        for meal_type, meal_info in meal_plan_data.items():
            Meal.objects.create(
                meal_plan=meal_plan,
                meal_type=meal_type,
                name=meal_info['name'],
                description=meal_info['description'],
                calories=meal_info['calories'],
                protein=meal_info['protein'],
                carbs=meal_info['carbs'],
                fat=meal_info['fat'],
                ingredients=meal_info['ingredients'],
                preparation=meal_info['preparation']
            )
        
        return meal_plan.id
        
    except Exception as e:
        print(f"Error generating meal plan: {str(e)}")
        return None
