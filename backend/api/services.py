import requests
import json
import boto3
import logging
from django.conf import settings
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

def get_weather_data(location):
    """
    Fetch weather data for a given location using a public Weather API
    """
    api_key = settings.WEATHER_API_KEY
    url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        weather_data = response.json()
        
        return {
            'temperature': weather_data['main']['temp'],
            'weather_condition': weather_data['weather'][0]['main'],
            'humidity': weather_data['main']['humidity']
        }
    except requests.exceptions.RequestException as e:
        logger.error(f"Weather API error: {str(e)}")
        return {
            'temperature': 11.0,  # Default values if API fails
            'weather_condition': 'Windy',
            'humidity': 50
        }

def get_fitness_data(user_id, api_id):
    """
    Fetch fitness data from classmate's Fitness Tracker API
    """
    fitness_api_url = settings.FITNESS_API_URL
    fitness_api_key = settings.FITNESS_API_KEY
    
    url = f"{fitness_api_url}/fitness/{api_id}/daily"
    headers = {
        'Authorization': f'Bearer {fitness_api_key}',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        fitness_data = response.json()
        
        return {
            'calories_burned': fitness_data.get('calories_burned', 0),
            'steps': fitness_data.get('steps', 0),
            'active_minutes': fitness_data.get('active_minutes', 0)
        }
    except requests.exceptions.RequestException as e:
        logger.error(f"Fitness API error: {str(e)}")
        return {
            'calories_burned': 2000,  # Default values if API fails
            'steps': 5000,
            'active_minutes': 30
        }

def generate_meal_plan(user_profile, weather_data, fitness_data):
    """
    Generate meal plan using AWS Lambda function
    """
    # Create Lambda client without explicit credentials (relies on SSO)
    lambda_client = boto3.client('lambda', region_name=settings.AWS_REGION)
    
    # Prepare the payload for the Lambda function
    payload = {
        'user_data': {
            'age': user_profile.age,
            'gender': user_profile.gender,
            'height': user_profile.height,
            'weight': user_profile.weight,
            'activity_level': user_profile.activity_level,
            'dietary_preference': user_profile.dietary_preference,
            'allergies': user_profile.allergies.split(',') if user_profile.allergies else []
        },
        'weather_data': weather_data,
        'fitness_data': fitness_data
    }
    
    try:
        # Invoke the Lambda function
        response = lambda_client.invoke(
            FunctionName=settings.AWS_LAMBDA_FUNCTION_NAME,
            InvocationType='RequestResponse',
            Payload=json.dumps(payload)
        )
        
        # Parse the response
        result = json.loads(response['Payload'].read().decode())
        return result
    except Exception as e:
        logger.error(f"AWS Lambda error: {str(e)}")
        # Return a basic meal plan as fallback
        return {
            'breakfast': {
                'name': 'Default Breakfast',
                'description': 'A balanced breakfast option',
                'calories': 500,
                'protein': 20,
                'carbs': 60,
                'fat': 15,
                'ingredients': 'Eggs, Whole grain bread, Avocado',
                'preparation': 'Prepare eggs as desired. Toast bread. Slice avocado and serve together.'
            },
            'lunch': {
                'name': 'Default Lunch',
                'description': 'A nutritious lunch option',
                'calories': 700,
                'protein': 30,
                'carbs': 80,
                'fat': 20,
                'ingredients': 'Chicken breast, Brown rice, Mixed vegetables',
                'preparation': 'Grill chicken. Cook rice. Steam vegetables. Serve together.'
            },
            'dinner': {
                'name': 'Default Dinner',
                'description': 'A wholesome dinner option',
                'calories': 600,
                'protein': 35,
                'carbs': 50,
                'fat': 20,
                'ingredients': 'Salmon fillet, Quinoa, Spinach',
                'preparation': 'Bake salmon. Cook quinoa. Sauté spinach. Plate and serve.'
            },
            'snack': {
                'name': 'Default Snack',
                'description': 'A healthy snack option',
                'calories': 200,
                'protein': 10,
                'carbs': 20,
                'fat': 8,
                'ingredients': 'Greek yogurt, Berries, Honey',
                'preparation': 'Mix yogurt with berries and a drizzle of honey.'
            }
        }