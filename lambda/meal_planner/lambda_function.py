import json
import random

def get_base_calorie_needs(user_data):
    """Calculate base calorie needs using the Harris-Benedict equation"""
    age = user_data.get('age', 30)
    gender = user_data.get('gender', 'male')
    weight = user_data.get('weight', 70)  # kg
    height = user_data.get('height', 170)  # cm
    
    if gender == 'male':
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    
    return bmr

def get_activity_multiplier(activity_level):
    """Return activity multiplier based on user's activity level"""
    multipliers = {
        'sedentary': 1.2,
        'light': 1.375,
        'moderate': 1.55,
        'active': 1.725,
        'very_active': 1.9
    }
    return multipliers.get(activity_level, 1.55)

def adjust_for_weather(calories, weather_data):
    """Adjust calories based on weather conditions"""
    temperature = weather_data.get('temperature', 20)
    condition = weather_data.get('weather_condition', 'Clear').lower()
    
    # Temperature adjustments
    if temperature < 10:  # Cold weather
        calories *= 1.05  # Increase by 5% for cold weather
    elif temperature > 30:  # Hot weather
        calories *= 0.95  # Decrease by 5% for hot weather
    
    # Weather condition adjustments
    if 'rain' in condition or 'snow' in condition:
        # Comfort foods for rainy/snowy days
        meal_preferences = {
            'breakfast': ['Oatmeal', 'Warm Breakfast Bowl'],
            'lunch': ['Hearty Soup', 'Stew'],
            'dinner': ['Casserole', 'Warm Bowl'],
            'snack': ['Hot Chocolate', 'Warm Nuts']
        }
    else:
        # Regular options
        meal_preferences = {
            'breakfast': ['Smoothie Bowl', 'Egg Breakfast'],
            'lunch': ['Salad Bowl', 'Sandwich'],
            'dinner': ['Grilled Protein', 'Rice Bowl'],
            'snack': ['Fruit Plate', 'Yogurt']
        }
    
    return calories, meal_preferences

def adjust_for_fitness(calories, fitness_data):
    """Adjust calories based on fitness activity"""
    calories_burned = fitness_data.get('calories_burned', 0)
    steps = fitness_data.get('steps', 0)
    
    # If the user is very active (high step count or calories burned)
    if steps > 10000 or calories_burned > 500:
        calories += 300  # Add more calories for active users
        protein_ratio = 0.3  # Higher protein ratio
    else:
        protein_ratio = 0.25  # Standard protein ratio
    
    return calories, protein_ratio

def generate_meal(meal_type, calories, protein_ratio, dietary_preference, meal_name_preference=None):
    """Generate a meal based on type, calories, and dietary preference"""
    carb_ratio = 0.5 if meal_type == 'breakfast' else 0.4
    fat_ratio = 1 - protein_ratio - carb_ratio
    
    # Calorie distribution across meals
    meal_calorie_distribution = {
        'breakfast': 0.25,
        'lunch': 0.35,
        'dinner': 0.3,
        'snack': 0.1
    }
    
    meal_calories = calories * meal_calorie_distribution[meal_type]
    
    # Calculate macros
    protein_grams = (meal_calories * protein_ratio) / 4  # 4 calories per gram of protein
    carb_grams = (meal_calories * carb_ratio) / 4  # 4 calories per gram of carb
    fat_grams = (meal_calories * fat_ratio) / 9  # 9 calories per gram of fat
    
    # Meal database (simplified for this example)
    meal_options = {
        'omnivore': {
            'breakfast': [
                {
                    'name': 'Scrambled Eggs with Toast',
                    'description': 'Fluffy scrambled eggs with whole grain toast and avocado',
                    'ingredients': 'Eggs, Whole grain bread, Avocado, Salt, Pepper',
                    'preparation': 'Whisk eggs with salt and pepper. Scramble in a non-stick pan. Toast bread and serve with sliced avocado.'
                },
                {
                    'name': 'Greek Yogurt Parfait',
                    'description': 'Creamy Greek yogurt with mixed berries and granola',
                    'ingredients': 'Greek yogurt, Mixed berries, Granola, Honey',
                    'preparation': 'Layer yogurt, berries, and granola in a bowl. Drizzle with honey.'
                }
            ],
            'lunch': [
                {
                    'name': 'Grilled Chicken Salad',
                    'description': 'Grilled chicken breast over mixed greens with vinaigrette',
                    'ingredients': 'Chicken breast, Mixed greens, Cherry tomatoes, Cucumber, Olive oil, Balsamic vinegar',
                    'preparation': 'Grill chicken. Toss vegetables with olive oil and vinegar. Serve chicken over greens.'
                },
                {
                    'name': 'Turkey and Avocado Wrap',
                    'description': 'Lean turkey with avocado and vegetables in a whole grain wrap',
                    'ingredients': 'Turkey slices, Avocado, Whole grain wrap, Lettuce, Tomato, Mustard',
                    'preparation': 'Lay out wrap. Layer with turkey, avocado, and vegetables. Roll up and slice.'
                }
            ],
            'dinner': [
                {
                    'name': 'Baked Salmon with Quinoa',
                    'description': 'Herb-baked salmon fillet with fluffy quinoa and steamed vegetables',
                    'ingredients': 'Salmon fillet, Quinoa, Broccoli, Lemon, Herbs, Olive oil',
                    'preparation': 'Bake salmon with herbs and lemon. Cook quinoa according to package. Steam broccoli. Serve together.'
                },
                {
                    'name': 'Lean Beef Stir Fry',
                    'description': 'Lean beef strips stir-fried with colorful vegetables and brown rice',
                    'ingredients': 'Lean beef, Brown rice, Bell peppers, Broccoli, Carrots, Soy sauce, Ginger, Garlic',
                    'preparation': 'Cook brown rice. Stir-fry beef with garlic and ginger. Add vegetables and soy sauce. Serve over rice.'
                }
            ],
            'snack': [
                {
                    'name': 'Apple with Almond Butter',
                    'description': 'Crisp apple slices with creamy almond butter',
                    'ingredients': 'Apple, Almond butter',
                    'preparation': 'Slice apple and serve with a side of almond butter for dipping.'
                },
                {
                    'name': 'Mixed Nuts and Dried Fruit',
                    'description': 'Energy-boosting mix of nuts and dried fruit',
                    'ingredients': 'Almonds, Walnuts, Cashews, Dried cranberries, Dried apricots',
                    'preparation': 'Mix all ingredients in a small container.'
                }
            ]
        },
        'vegetarian': {
            # Similar structure with vegetarian options
            'breakfast': [
                {
                    'name': 'Veggie Omelette',
                    'description': 'Fluffy omelette with sautéed vegetables and cheese',
                    'ingredients': 'Eggs, Bell peppers, Spinach, Onion, Cheese, Salt, Pepper',
                    'preparation': 'Whisk eggs. Sauté vegetables. Pour eggs over vegetables and cook. Fold in half and serve.'
                }
            ],
            'lunch': [
                {
                    'name': 'Mediterranean Quinoa Bowl',
                    'description': 'Protein-rich quinoa with Mediterranean vegetables and feta cheese',
                    'ingredients': 'Quinoa, Cucumber, Cherry tomatoes, Olives, Feta cheese, Olive oil, Lemon juice',
                    'preparation': 'Cook quinoa. Chop vegetables. Mix all ingredients with olive oil and lemon juice.'
                }
            ],
            'dinner': [
                {
                    'name': 'Vegetable Stir Fry with Tofu',
                    'description': 'Crispy tofu with colorful vegetables in a savory sauce',
                    'ingredients': 'Tofu, Brown rice, Mixed vegetables, Soy sauce, Ginger, Garlic',
                    'preparation': 'Press and cube tofu. Cook rice. Stir-fry tofu until crispy. Add vegetables and sauce.'
                }
            ],
            'snack': [
                {
                    'name': 'Hummus with Veggie Sticks',
                    'description': 'Creamy hummus with fresh vegetable sticks',
                    'ingredients': 'Hummus, Carrots, Celery, Bell peppers',
                    'preparation': 'Cut vegetables into sticks. Serve with a side of hummus.'
                }
            ]
        },
        'vegan': {
            # Vegan meal options
            'breakfast': [
                {
                    'name': 'Vegan Smoothie Bowl',
                    'description': 'Thick fruit smoothie topped with granola and seeds',
                    'ingredients': 'Banana, Berries, Almond milk, Maple syrup, Granola, Chia seeds',
                    'preparation': 'Blend fruit with almond milk. Pour into bowl. Top with granola and seeds.'
                }
            ],
            'lunch': [
                {
                    'name': 'Chickpea Avocado Sandwich',
                    'description': 'Mashed chickpea and avocado on whole grain bread',
                    'ingredients': 'Chickpeas, Avocado, Whole grain bread, Lettuce, Tomato, Lemon juice',
                    'preparation': 'Mash chickpeas and avocado with lemon juice. Spread on bread. Add vegetables.'
                }
            ],
            'dinner': [
                {
                    'name': 'Lentil Curry with Brown Rice',
                    'description': 'Spiced lentil curry with fluffy brown rice',
                    'ingredients': 'Lentils, Brown rice, Coconut milk, Curry spices, Onion, Garlic, Vegetables',
                    'preparation': 'Cook lentils. Sauté vegetables with spices. Add coconut milk. Serve over rice.'
                }
            ],
            'snack': [
                {
                    'name': 'Energy Balls',
                    'description': 'No-bake energy balls with dates and nuts',
                    'ingredients': 'Dates, Nuts, Oats, Coconut flakes, Cocoa powder',
                    'preparation': 'Process dates and nuts. Mix with other ingredients. Roll into balls. Refrigerate.'
                }
            ]
        },
        'keto': {
            # Keto meal options
            'breakfast': [
                {
                    'name': 'Avocado and Bacon Eggs',
                    'description': 'Fried eggs with avocado and crispy bacon',
                    'ingredients': 'Eggs, Avocado, Bacon, Butter, Salt, Pepper',
                    'preparation': 'Fry bacon until crispy. Cook eggs in bacon fat. Serve with sliced avocado.'
                }
            ],
            'lunch': [
                {
                    'name': 'Keto Cobb Salad',
                    'description': 'Low-carb salad with avocado, eggs, bacon, and blue cheese',
                    'ingredients': 'Lettuce, Avocado, Hard-boiled eggs, Bacon, Blue cheese, Olive oil, Vinegar',
                    'preparation': 'Arrange lettuce. Top with chopped eggs, bacon, avocado, and cheese. Dress with oil and vinegar.'
                }
            ],
            'dinner': [
                {
                    'name': 'Baked Salmon with Asparagus',
                    'description': 'Fatty fish with low-carb vegetables',
                    'ingredients': 'Salmon fillet, Asparagus, Butter, Lemon, Herbs, Salt, Pepper',
                    'preparation': 'Bake salmon and asparagus with butter, lemon, and herbs until fish flakes easily.'
                }
            ],
            'snack': [
                {
                    'name': 'Cheese and Olive Plate',
                    'description': 'Assorted cheeses with olives and nuts',
                    'ingredients': 'Cheese varieties, Olives, Almonds',
                    'preparation': 'Arrange cheese, olives, and nuts on a plate.'
                }
            ]
        },
        'paleo': {
            # Paleo meal options
            'breakfast': [
                {
                    'name': 'Sweet Potato Hash with Eggs',
                    'description': 'Sweet potato hash with fried eggs',
                    'ingredients': 'Sweet potato, Eggs, Onion, Bell pepper, Olive oil, Herbs',
                    'preparation': 'Sauté diced sweet potato with vegetables until soft. Top with fried eggs.'
                }
            ],
            'lunch': [
                {
                    'name': 'Tuna Avocado Lettuce Wraps',
                    'description': 'Tuna salad wrapped in lettuce leaves',
                    'ingredients': 'Tuna, Avocado, Lettuce leaves, Red onion, Olive oil, Lemon juice',
                    'preparation': 'Mix tuna with mashed avocado, diced onion, olive oil, and lemon juice. Wrap in lettuce leaves.'
                }
            ],
            'dinner': [
                {
                    'name': 'Grilled Steak with Roasted Vegetables',
                    'description': 'Grass-fed steak with colorful roasted vegetables',
                    'ingredients': 'Steak, Zucchini, Bell peppers, Carrots, Olive oil, Herbs',
                    'preparation': 'Grill steak to desired doneness. Roast vegetables with olive oil and herbs.'
                }
            ],
            'snack': [
                {
                    'name': 'Apple Slices with Almond Butter',
                    'description': 'Fresh apple with natural almond butter',
                    'ingredients': 'Apple, Almond butter',
                    'preparation': 'Slice apple and serve with a side of almond butter.'
                }
            ]
        }
    }
    
    # Select a meal preferentially from the weather-based preferences if available
    options = meal_options.get(dietary_preference, meal_options['omnivore'])[meal_type]
    
    if meal_name_preference and any(meal['name'].startswith(pref) for pref in meal_name_preference for meal in options):
        filtered_options = [meal for meal in options if any(meal['name'].startswith(pref) for pref in meal_name_preference)]
        selected_meal = random.choice(filtered_options)
    else:
        selected_meal = random.choice(options)
    
    # Adjust the meal for the calculated calories and macros
    selected_meal['calories'] = round(meal_calories)
    selected_meal['protein'] = round(protein_grams, 1)
    selected_meal['carbs'] = round(carb_grams, 1)
    selected_meal['fat'] = round(fat_grams, 1)
    
    return selected_meal

def lambda_handler(event, context):
    """Main Lambda function handler"""
    try:
        # Extract data from the event
        user_data = event.get('user_data', {})
        weather_data = event.get('weather_data', {})
        fitness_data = event.get('fitness_data', {})
        
        # Get user's dietary preference
        dietary_preference = user_data.get('dietary_preference', 'omnivore')
        
        # Calculate base calorie needs
        base_calories = get_base_calorie_needs(user_data)
        
        # Adjust for activity level
        activity_level = user_data.get('activity_level', 'moderate')
        adjusted_calories = base_calories * get_activity_multiplier(activity_level)
        
        # Adjust for weather
        weather_adjusted_calories, meal_preferences = adjust_for_weather(adjusted_calories, weather_data)
        
        # Adjust for fitness data
        final_calories, protein_ratio = adjust_for_fitness(weather_adjusted_calories, fitness_data)
        
        # Generate meal plan
        meal_plan = {
            'breakfast': generate_meal('breakfast', final_calories, protein_ratio, dietary_preference, meal_preferences.get('breakfast')),
            'lunch': generate_meal('lunch', final_calories, protein_ratio, dietary_preference, meal_preferences.get('lunch')),
            'dinner': generate_meal('dinner', final_calories, protein_ratio, dietary_preference, meal_preferences.get('dinner')),
            'snack': generate_meal('snack', final_calories, protein_ratio, dietary_preference, meal_preferences.get('snack'))
        }
        
        # Return the generated meal plan
        return meal_plan
        
    except Exception as e:
        # Log the error and return a default response
        print(f"Error: {str(e)}")
        return {
            'error': str(e)
        }