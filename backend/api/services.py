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
            'temperature': 20.0,  # Default values if API fails
            'weather_condition': 'Unknown',
            'humidity': 50
        }
        
""" for the testing purpose as my friend's API does not contain the specific fieleds yet I needed to generate the meal plan
def get_fitness_data(user_id, api_id):
    
    # Fetch fitness data from classmate's Fitness Tracker API

    fitness_api_url = settings.FITNESS_API_URL
    
    # Log the request details for debugging
    logger.info(f"Attempting to fetch fitness data for user_id: {user_id}, api_id: {api_id}")
    
    if not api_id:
        logger.error(f"No fitness_api_id provided for user {user_id}")
        return {
            'calories_burned': 2000,  # Default values if API fails
            'steps': 5000,
            'active_minutes': 30,
            'using_default': True  # Flag to indicate default values are being used
        }
    
    # api_id is a string to match the format in the API response
    api_id = str(api_id)
    logger.info(f"Looking for member with ID: {api_id}")
    
    # For this API, don't need to construct a per-user URL
    # fetch all members and find the one matching the api_id
    url = fitness_api_url
    
    try:
        response = requests.get(url)
        # Log the response status
        logger.info(f"Fitness API response status: {response.status_code}")
        
        if response.status_code != 200:
            logger.error(f"Fitness API error: {response.text if hasattr(response, 'text') else 'No response text'}")
            raise requests.exceptions.RequestException(f"API returned {response.status_code}")
        
        # Parse the response
        data = response.json()
        logger.info(f"Fitness API response: {data}")
        
        # Check if the response has the expected structure
        if "body" in data and isinstance(data["body"], list):
            members = data["body"]
            
            # Log all available member IDs for debugging
            member_ids = [m.get("memberid") for m in members]
            logger.info(f"Available member IDs: {member_ids}")
            
            # Find the member with the matching ID
            member = next((m for m in members if m.get("memberid") == api_id), None)
            logger.info(f"Found member: {member}")
            
            # If no match, use the first member as a fallback
            if not member and members:
                logger.warning(f"Member with ID {api_id} not found. Using first available member instead.")
                member = members[0]
            
            if member:
                logger.info(f"Using fitness data for member: {member.get('name', 'Unknown')}")
                
                # Map fitness class to activity level
                fitness_class = member.get("fitness_class", "B")
                activity_level = map_fitness_class_to_activity(fitness_class)
                
                # Use age to estimate calorie needs
                try:
                    age = int(member.get("age", 25))
                except (ValueError, TypeError):
                    age = 25  # Default if age is not a valid number
                
                estimated_calories = estimate_calories_by_age(age, activity_level)
                
                # Return derived fitness data
                return {
                    'calories_burned': int(estimated_calories * 0.3),
                    'steps': int(estimated_calories * 2.5),
                    'active_minutes': estimate_active_minutes(activity_level),
                    'using_default': False
                }
            else:
                logger.error(f"No members found in fitness data")
        else:
            logger.error("Unexpected fitness API response structure")
            
        # If we reach here, something went wrong with finding or processing the member data
        raise Exception("Could not process fitness data")
            
    except Exception as e:
        logger.error(f"Fitness API error: {str(e)}")
        return {
            'calories_burned': 2000,  # Default values if API fails
            'steps': 5000,
            'active_minutes': 30,
            'using_default': True  # Flag to indicate default values are being used
        }

def map_fitness_class_to_activity(fitness_class):
    # Map fitness class (A, B, C) to activity level
    mapping = {
        "A": "active",
        "B": "moderate",
        "C": "light",
        # Default
        "": "moderate"
    }
    return mapping.get(fitness_class, "moderate")

def estimate_calories_by_age(age, activity_level):
    # Estimate base calories based on age and activity level
    # Very rough estimate - would be better with height/weight
    base_calories = 2000  # Default for adult
    
    # Age adjustments
    if age < 18:
        base_calories = 1800
    elif age > 50:
        base_calories = 1900
    
    # Activity multipliers
    multipliers = {
        "sedentary": 1.2,
        "light": 1.375,
        "moderate": 1.55,
        "active": 1.725,
        "very_active": 1.9
    }
    
    return int(base_calories * multipliers.get(activity_level, 1.55))

def estimate_active_minutes(activity_level):
    #Estimate active minutes based on activity level
    mapping = {
        "sedentary": 15,
        "light": 30,
        "moderate": 45,
        "active": 60,
        "very_active": 90
    }
    return mapping.get(activity_level, 45)
    
"""
def get_fitness_data(user_id, api_id):
    """
    Fetch fitness data from classmate's Fitness Tracker API
    """
    fitness_api_url = settings.FITNESS_API_URL
    fitness_api_key = settings.FITNESS_API_KEY
    
    # Log the request details for debugging
    logger.info(f"Attempting to fetch fitness data for user_id: {user_id}, api_id: {api_id}")
    
    if not api_id:
        logger.error(f"No fitness_api_id provided for user {user_id}")
        return {
            'calories_burned': 2000,  # Default values if API fails
            'steps': 5000,
            'active_minutes': 30,
            'using_default': True  # Flag to indicate default values are being used
        }
    
    url = f"{fitness_api_url}/fitness/{api_id}/daily"
    headers = {
        'Authorization': f'Bearer {fitness_api_key}',
        'Content-Type': 'application/json'
    }
    
    logger.info(f"Request URL: {url}")
    logger.info(f"Using API key: {'*' * (len(fitness_api_key) - 4) + fitness_api_key[-4:] if fitness_api_key else 'No API key set'}")
    
    if not fitness_api_url or fitness_api_url == 'https://your-classmates-fitness-api.com/api':
        logger.error("Fitness API URL is not properly configured")
        return {
            'calories_burned': 2000,  # Default values if API fails
            'steps': 5000,
            'active_minutes': 30,
            'using_default': True  # Flag to indicate default values are being used
        }
    
    try:
        response = requests.get(url, headers=headers)
        # Log the response status and content for debugging
        logger.info(f"Fitness API response status: {response.status_code}")
        
        if response.status_code != 200:
            logger.error(f"Fitness API error: {response.text if hasattr(response, 'text') else 'No response text'}")
            raise requests.exceptions.RequestException(f"API returned {response.status_code}")
            
        fitness_data = response.json()
        logger.info(f"Fitness data retrieved successfully: {fitness_data}")
        
        return {
            'calories_burned': fitness_data.get('calories_burned', 0),
            'steps': fitness_data.get('steps', 0),
            'active_minutes': fitness_data.get('active_minutes', 0),
            'using_default': False  # Flag to indicate actual values are being used
        }
    except requests.exceptions.RequestException as e:
        logger.error(f"Fitness API error: {str(e)}")
        return {
            'calories_burned': 2000,  # Default values if API fails
            'steps': 5000,
            'active_minutes': 30,
            'using_default': True  # Flag to indicate default values are being used
        }

def generate_meal_plan(user_profile, weather_data, fitness_data):
    """
    Generate meal plan using AWS Lambda function
    """
    # Create Lambda client without explicit credentials
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