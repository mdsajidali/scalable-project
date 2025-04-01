import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import axios from 'axios';
import { API_BASE_URL } from '../config';

const MealPlanView = () => {
  const { id } = useParams();
  const [mealPlan, setMealPlan] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  useEffect(() => {
    const fetchMealPlan = async () => {
      try {
        const response = await axios.get(`${API_BASE_URL}/api/meal-plans/${id}/`);
        setMealPlan(response.data);
      } catch (error) {
        console.error('Error fetching meal plan:', error);
        setError('Failed to load meal plan. Please try again later.');
      } finally {
        setLoading(false);
      }
    };
    
    fetchMealPlan();
  }, [id]);
  
  if (loading) {
    return <div className="text-center mt-5"><div className="spinner-border" role="status"></div></div>;
  }
  
  if (error) {
    return <div className="alert alert-danger mt-4">{error}</div>;
  }
  
  if (!mealPlan) {
    return <div className="alert alert-warning mt-4">Meal plan not found</div>;
  }
  
  // Helper to format meal type for display
  const formatMealType = (type) => {
    return type.charAt(0).toUpperCase() + type.slice(1);
  };
  
  return (
    <div className="meal-plan-container">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h1>Meal Plan Details</h1>
        <Link to="/dashboard" className="btn btn-outline-secondary">
          Back to Dashboard
        </Link>
      </div>
      
      {/* Meal Plan Header */}
      <div className="card mb-4">
        <div className="card-body">
          <div className="row">
            <div className="col-md-8">
              <h2 className="card-title">
                Meal Plan for {mealPlan.location}
                <span className="badge bg-info ms-2">{mealPlan.weather_condition}</span>
              </h2>
              <p>
                <strong>Created:</strong> {new Date(mealPlan.created_at).toLocaleString()}
              </p>
            </div>
            <div className="col-md-4">
              <div className="stats">
                <div className="stat-item">
                  <span className="stat-label">Temperature</span>
                  <span className="stat-value">{mealPlan.temperature}°C</span>
                </div>
                <div className="stat-item">
                  <span className="stat-label">Calories Burned</span>
                  <span className="stat-value">{mealPlan.calories_burned}</span>
                </div>
                <div className="stat-item">
                  <span className="stat-label">Steps</span>
                  <span className="stat-value">{mealPlan.steps}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      {/* Meals */}
      <div className="meals-container">
        <h3 className="mb-4">Today's Meals</h3>
        
        {/* Filter and sort meals by type */}
        {['breakfast', 'lunch', 'dinner', 'snack'].map(mealType => {
          const meal = mealPlan.meals?.find(m => m.meal_type === mealType);
          
          if (!meal) return null;
          
          return (
            <div className="card mb-4" key={meal.id}>
              <div className="card-header bg-light">
                <h4>{formatMealType(meal.meal_type)}</h4>
              </div>
              <div className="card-body">
                <h5 className="card-title">{meal.name}</h5>
                <p className="card-text">{meal.description}</p>
                
                <div className="row mb-4">
                  <div className="col-md-6">
                    <h6>Nutrition Information</h6>
                    <table className="table table-sm">
                      <tbody>
                        <tr>
                          <th>Calories</th>
                          <td>{meal.calories}</td>
                        </tr>
                        <tr>
                          <th>Protein</th>
                          <td>{meal.protein}g</td>
                        </tr>
                        <tr>
                          <th>Carbs</th>
                          <td>{meal.carbs}g</td>
                        </tr>
                        <tr>
                          <th>Fat</th>
                          <td>{meal.fat}g</td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </div>
                
                <h6>Ingredients</h6>
                <p>{meal.ingredients}</p>
                
                <h6>Preparation</h6>
                <p>{meal.preparation}</p>
              </div>
            </div>
          );
        })}
      </div>
      
      {/* Share Link */}
      <div className="card mt-4">
        <div className="card-body">
          <h5 className="card-title">Share This Meal Plan</h5>
          <p>
            Your classmates can access this meal plan through your public API endpoint:
          </p>
          <div className="input-group">
            <input 
              type="text" 
              className="form-control"
              value={`${API_BASE_URL}/api/public/users/${mealPlan.user}/meal-plans/${mealPlan.id}/`}
              readOnly
            />
            <button 
              className="btn btn-outline-secondary" 
              type="button"
              onClick={() => {
                navigator.clipboard.writeText(
                  `${API_BASE_URL}/api/public/users/${mealPlan.user}/meal-plans/${mealPlan.id}/`
                );
                alert('API URL copied to clipboard!');
              }}
            >
              Copy
            </button>
          </div>
          <small className="text-muted mt-2 d-block">
            This is a public endpoint that can be accessed without authentication.
          </small>
        </div>
      </div>
    </div>
  );
};

export default MealPlanView;