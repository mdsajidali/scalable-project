import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';
import { API_BASE_URL } from '../config';

const Dashboard = () => {
  const { currentUser } = useAuth();
  const [mealPlans, setMealPlans] = useState([]);
  const [latestMealPlan, setLatestMealPlan] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [location, setLocation] = useState('');
  const [generating, setGenerating] = useState(false);
  const [generationMessage, setGenerationMessage] = useState('');
  const [warnings, setWarnings] = useState([]);
  const [showManualEntry, setShowManualEntry] = useState(false);
  const [manualFitnessData, setManualFitnessData] = useState({
    calories_burned: 2000,
    steps: 5000,
    active_minutes: 30
  });
  
  // Fetch meal plans on component mount
  useEffect(() => {
    const fetchMealPlans = async () => {
      try {
        const response = await axios.get(`${API_BASE_URL}/api/meal-plans/`);
        setMealPlans(response.data);
        
        // Try to get the latest meal plan
        const latestResponse = await axios.get(`${API_BASE_URL}/api/meal-plans/latest/`);
        setLatestMealPlan(latestResponse.data);
      } catch (error) {
        console.error('Error fetching meal plans:', error);
        setError('Failed to fetch meal plans. Please try again later.');
      } finally {
        setLoading(false);
      }
    };
    
    fetchMealPlans();
  }, []);
  
  const handleManualFitnessChange = (e) => {
    const { name, value } = e.target;
    setManualFitnessData({
      ...manualFitnessData,
      [name]: parseInt(value, 10) || 0
    });
  };
  
  // Handle meal plan generation
  const handleGenerateMealPlan = async (e) => {
    e.preventDefault();
    
    if (!location) {
      setError('Please enter your location');
      return;
    }
    
    setGenerating(true);
    setGenerationMessage('Generating your personalized meal plan...');
    setError(null);
    setWarnings([]);
    
    try {
      // Include manual fitness data if the user has entered it
      const requestData = {
        location
      };
      
      if (showManualEntry) {
        requestData.manual_fitness_data = manualFitnessData;
      }
      
      const response = await axios.post(`${API_BASE_URL}/api/meal-plans/generate/`, requestData);
      
      // Check for warnings
      if (response.data.warnings && response.data.warnings.length > 0) {
        setWarnings(response.data.warnings);
      }
      
      setGenerationMessage('Your meal plan is being generated! It will appear here shortly.');
      
      // Poll for the new meal plan
      const pollInterval = setInterval(async () => {
        try {
          const latestResponse = await axios.get(`${API_BASE_URL}/api/meal-plans/latest/`);
          
          // If we have a new meal plan with a different ID than before
          if (latestResponse.data && (!latestMealPlan || latestResponse.data.id !== latestMealPlan.id)) {
            setLatestMealPlan(latestResponse.data);
            setMealPlans(prevPlans => [latestResponse.data, ...prevPlans]);
            setGenerationMessage('');
            setGenerating(false);
            clearInterval(pollInterval);
          }
        } catch (error) {
          console.error('Error polling for meal plan:', error);
        }
      }, 3000); // Poll every 3 seconds
      
      // Stop polling after 30 seconds if no result
      setTimeout(() => {
        clearInterval(pollInterval);
        if (generating) {
          setGenerating(false);
          setGenerationMessage('');
          setError('Meal plan generation is taking longer than expected. Please check back later.');
        }
      }, 30000);
      
    } catch (error) {
      console.error('Error generating meal plan:', error);
      setError('Failed to generate meal plan. Please try again later.');
      setGenerating(false);
      setGenerationMessage('');
      
      // Check for warnings in the error response
      if (error.response && error.response.data && error.response.data.warnings) {
        setWarnings(error.response.data.warnings);
      }
    }
  };
  
  if (loading) {
    return <div className="text-center mt-5"><div className="spinner-border" role="status"></div></div>;
  }
  
  return (
    <div className="dashboard-container">
      <div className="row">
        <div className="col-md-8">
          <h1>Welcome, {currentUser?.firstName || currentUser?.username}!</h1>
          <p>Generate a personalized meal plan based on your fitness data and current weather conditions.</p>
        </div>
        <div className="col-md-4">
          <div className="card">
            <div className="card-body">
              <h5 className="card-title">Generate New Meal Plan</h5>
              {error && <div className="alert alert-danger">{error}</div>}
              {warnings.length > 0 && (
                <div className="alert alert-warning">
                  {warnings.map((warning, index) => (
                    <p key={index} className="mb-1">{warning}</p>
                  ))}
                  {warnings.some(w => w.includes("fitness data")) && (
                    <button 
                      className="btn btn-sm btn-outline-secondary mt-2" 
                      onClick={() => setShowManualEntry(!showManualEntry)}
                    >
                      {showManualEntry ? 'Hide Manual Entry' : 'Enter Fitness Data Manually'}
                    </button>
                  )}
                </div>
              )}
              {generationMessage && <div className="alert alert-info">{generationMessage}</div>}
              <form onSubmit={handleGenerateMealPlan}>
                <div className="mb-3">
                  <label htmlFor="location" className="form-label">Your Location</label>
                  <input
                    type="text"
                    className="form-control"
                    id="location"
                    placeholder="e.g., Dublin, Ireland"
                    value={location}
                    onChange={(e) => setLocation(e.target.value)}
                    required
                  />
                  <div className="form-text">We'll use this to check local weather conditions</div>
                </div>
                
                {/* Manual Fitness Data Entry */}
                {showManualEntry && (
                  <div className="manual-fitness-data mb-3">
                    <h6 className="mb-2">Manual Fitness Data Entry</h6>
                    <div className="row g-2">
                      <div className="col-md-4">
                        <label htmlFor="calories_burned" className="form-label">Calories Burned</label>
                        <input
                          type="number"
                          className="form-control"
                          id="calories_burned"
                          name="calories_burned"
                          value={manualFitnessData.calories_burned}
                          onChange={handleManualFitnessChange}
                          min="0"
                        />
                      </div>
                      <div className="col-md-4">
                        <label htmlFor="steps" className="form-label">Steps</label>
                        <input
                          type="number"
                          className="form-control"
                          id="steps"
                          name="steps"
                          value={manualFitnessData.steps}
                          onChange={handleManualFitnessChange}
                          min="0"
                        />
                      </div>
                      <div className="col-md-4">
                        <label htmlFor="active_minutes" className="form-label">Active Minutes</label>
                        <input
                          type="number"
                          className="form-control"
                          id="active_minutes"
                          name="active_minutes"
                          value={manualFitnessData.active_minutes}
                          onChange={handleManualFitnessChange}
                          min="0"
                        />
                      </div>
                    </div>
                  </div>
                )}
                
                <button 
                  type="submit" 
                  className="btn btn-primary w-100"
                  disabled={generating}
                >
                  {generating ? 'Generating...' : 'Generate Meal Plan'}
                </button>
              </form>
            </div>
          </div>
        </div>
      </div>
      
      {/* Latest Meal Plan Section */}
      {latestMealPlan && (
        <div className="latest-meal-plan mt-4">
          <h2>Your Latest Meal Plan</h2>
          <div className="card">
            <div className="card-body">
              <h5 className="card-title">
                Meal Plan for {latestMealPlan.location}
                <span className="badge bg-info ms-2">{latestMealPlan.weather_condition}</span>
                <span className="badge bg-secondary ms-2">{latestMealPlan.temperature}°C</span>
              </h5>
              <p className="card-text">
                <small className="text-muted">Created on {new Date(latestMealPlan.created_at).toLocaleDateString()}</small>
              </p>
              
              {/* Activity data */}
              <div className="activity-data mb-3">
                <span className="badge bg-primary me-2">
                  Calories Burned: {latestMealPlan.calories_burned}
                </span>
                <span className="badge bg-primary">
                  Steps: {latestMealPlan.steps}
                </span>
              </div>
              
              {/* Basic display of meals */}
              <div className="row">
                {latestMealPlan.meals && latestMealPlan.meals.map(meal => (
                  <div className="col-md-6 mb-3" key={meal.id}>
                    <div className="card h-100">
                      <div className="card-header bg-light">
                        {meal.meal_type.charAt(0).toUpperCase() + meal.meal_type.slice(1)}
                      </div>
                      <div className="card-body">
                        <h6 className="card-title">{meal.name}</h6>
                        <p className="card-text">{meal.description}</p>
                        <div className="d-flex justify-content-between">
                          <div><strong>Calories:</strong> {meal.calories}</div>
                          <div><strong>Protein:</strong> {meal.protein}g</div>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
              
              <div className="text-center mt-3">
                <Link to={`/meal-plans/${latestMealPlan.id}`} className="btn btn-outline-primary">
                  View Full Details
                </Link>
              </div>
            </div>
          </div>
        </div>
      )}
      
      {/* Previous Meal Plans */}
      {mealPlans.length > 0 && (
        <div className="previous-meal-plans mt-4">
          <h2>Previous Meal Plans</h2>
          <div className="list-group">
            {mealPlans.map(plan => (
              <Link
                to={`/meal-plans/${plan.id}`}
                className="list-group-item list-group-item-action"
                key={plan.id}
              >
                <div className="d-flex w-100 justify-content-between">
                  <h5 className="mb-1">
                    Meal Plan for {plan.location}
                    <span className="badge bg-info ms-2">{plan.weather_condition}</span>
                  </h5>
                  <small>{new Date(plan.created_at).toLocaleDateString()}</small>
                </div>
                <p className="mb-1">
                  Temperature: {plan.temperature}°C | 
                  Calories Burned: {plan.calories_burned} | 
                  Steps: {plan.steps}
                </p>
              </Link>
            ))}
          </div>
        </div>
      )}
      
      {/* No meal plans message */}
      {mealPlans.length === 0 && !latestMealPlan && !generating && (
        <div className="alert alert-info mt-4">
          You don't have any meal plans yet. Generate your first plan using the form above!
        </div>
      )}
    </div>
  );
};

export default Dashboard;