import requests
import json

def test_fitness_api():
    """
    Test the fitness API and see how we could use it for meal planning
    """
    api_url = "https://l734p4kw4i.execute-api.eu-west-1.amazonaws.com/Prod"
    
    try:
        print(f"Fetching data from {api_url}...")
        response = requests.get(api_url)
        response.raise_for_status()
        
        print(f"Response status code: {response.status_code}")
        data = response.json()
        
        print("API response:")
        print(json.dumps(data, indent=2))
        
        # Check if the response structure is as expected
        if "body" in data and isinstance(data["body"], list):
            members = data["body"]
            
            print(f"\nFound {len(members)} fitness members")
            
            # Process each member to derive meal planning inputs
            for member in members:
                print(f"\nProcessing member: {member['name']}")
                
                # Map fitness class to activity level
                fitness_class = member.get("fitness_class", "B")
                activity_level = map_fitness_class_to_activity(fitness_class)
                
                # Use age to estimate calorie needs
                age = int(member.get("age", 25))
                estimated_calories = estimate_calories_by_age(age, activity_level)
                
                # Derive other metrics
                derived_data = {
                    "member_id": member.get("memberid"),
                    "name": member.get("name"),
                    "age": age,
                    "fitness_class": fitness_class,
                    "derived_activity_level": activity_level,
                    "estimated_daily_calories": estimated_calories,
                    "estimated_calories_burned": int(estimated_calories * 0.3),
                    "estimated_steps": int(estimated_calories * 2.5),
                    "estimated_active_minutes": estimate_active_minutes(activity_level)
                }
                
                print("Derived fitness data for meal planning:")
                print(json.dumps(derived_data, indent=2))
                
            return True
        else:
            print("Unexpected API response structure")
            return False
            
    except Exception as e:
        print(f"Error testing Fitness API: {str(e)}")
        return False

def map_fitness_class_to_activity(fitness_class):
    """Map fitness class (A, B, C) to activity level"""
    mapping = {
        "A": "active",
        "B": "moderate",
        "C": "light",
        # Default
        "": "moderate"
    }
    return mapping.get(fitness_class, "moderate")

def estimate_calories_by_age(age, activity_level):
    """Estimate base calories based on age and activity level"""
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
    """Estimate active minutes based on activity level"""
    mapping = {
        "sedentary": 15,
        "light": 30,
        "moderate": 45,
        "active": 60,
        "very_active": 90
    }
    return mapping.get(activity_level, 45)

# Run the test
if __name__ == "__main__":
    print("Testing Fitness API...")
    result = test_fitness_api()
    print(f"\nTest {'succeeded' if result else 'failed'}")