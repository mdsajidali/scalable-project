from django.db import models
from django.contrib.auth.models import User

class MealPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='meal_plans')
    created_at = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=100)
    temperature = models.FloatField(help_text="Temperature in Celsius")
    weather_condition = models.CharField(max_length=50)
    calories_burned = models.IntegerField()
    steps = models.IntegerField()
    
    def __str__(self):
        return f"Meal Plan for {self.user.username} on {self.created_at.strftime('%Y-%m-%d')}"

class Meal(models.Model):
    MEAL_TYPES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snack', 'Snack')
    ]
    
    meal_plan = models.ForeignKey(MealPlan, on_delete=models.CASCADE, related_name='meals')
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPES)
    name = models.CharField(max_length=200)
    description = models.TextField()
    calories = models.IntegerField()
    protein = models.FloatField(help_text="Protein in grams")
    carbs = models.FloatField(help_text="Carbohydrates in grams")
    fat = models.FloatField(help_text="Fat in grams")
    ingredients = models.TextField()
    preparation = models.TextField()
    
    def __str__(self):
        return f"{self.meal_type} - {self.name}"