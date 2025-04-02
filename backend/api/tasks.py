from celery import shared_task
from .models import MealPlan, Meal
from .services import get_weather_data, get_fitness_data, generate_meal_plan
from django.contrib.auth.models import User
import logging

logger = logging.getLogger(__name__)

# Regular function (Celery is optional to use)
def generate_meal_plan_task(user_id, location, manual_fitness_data=None):
    """
    Synchronous version of meal plan generation
    """
    from django.contrib.auth.models import User
    from .services import get_weather_data, get_fitness_data, generate_meal_plan
    from .models import MealPlan, Meal
    
    warnings = []
    
    try:
        user = User.objects.get(id=user_id)
        user_profile = user.profile
        
        # Get weather data
        weather_data = get_weather_data(location)
        if weather_data.get('weather_condition') == 'Unknown':
            warnings.append("Could not retrieve accurate weather data. Using default weather conditions.")
        
        # Get fitness data - either from API or manual entry
        if manual_fitness_data:
            # Use manually entered fitness data
            fitness_data = {
                'calories_burned': manual_fitness_data.get('calories_burned', 2000),
                'steps': manual_fitness_data.get('steps', 5000),
                'active_minutes': manual_fitness_data.get('active_minutes', 30),
                'using_default': False,  # Not using default values since user provided them
                'manual_entry': True     # Flag to indicate manual entry
            }
            warnings.append("Using manually entered fitness data for meal planning.")
        else:
            # Try to get fitness data from API
            fitness_data = get_fitness_data(user_id, user_profile.fitness_api_id)
            
            if fitness_data.get('using_default', False):
                warnings.append("Could not retrieve your fitness data. Using default activity values for meal planning.")
                warnings.append("You can provide your own fitness data by using the manual entry option.")
        
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
        
        return {
            'meal_plan_id': meal_plan.id,
            'warnings': warnings
        }
        
    except Exception as e:
        logger.error(f"Error generating meal plan: {str(e)}")
        return None