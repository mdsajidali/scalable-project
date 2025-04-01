import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';

const Profile = () => {
  const { currentUser, updateProfile } = useAuth();
  
  const [formData, setFormData] = useState({
    first_name: currentUser?.firstName || '',
    last_name: currentUser?.lastName || '',
    email: currentUser?.email || '',
    profile: {
      age: currentUser?.profile?.age || '',
      height: currentUser?.profile?.height || '',
      weight: currentUser?.profile?.weight || '',
      gender: currentUser?.profile?.gender || '',
      activity_level: currentUser?.profile?.activity_level || 'moderate',
      dietary_preference: currentUser?.profile?.dietary_preference || 'omnivore',
      allergies: currentUser?.profile?.allergies || '',
      fitness_api_id: currentUser?.profile?.fitness_api_id || '',
      location: currentUser?.profile?.location || ''
    }
  });
  
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [errors, setErrors] = useState({});
  
  const handleChange = (e) => {
    const { name, value } = e.target;
    
    // Check if this is a profile field
    if (name.startsWith('profile.')) {
      const profileField = name.split('.')[1];
      setFormData({
        ...formData,
        profile: {
          ...formData.profile,
          [profileField]: value
        }
      });
    } else {
      setFormData({
        ...formData,
        [name]: value
      });
    }
  };
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    setLoading(true);
    setSuccess(false);
    setErrors({});
    
    try {
      await updateProfile(formData);
      setSuccess(true);
      window.scrollTo(0, 0);
    } catch (error) {
      console.error('Update profile error:', error);
      
      // Handle API errors
      if (error.response && error.response.data) {
        setErrors(error.response.data);
      } else {
        setErrors({ general: 'An error occurred. Please try again.' });
      }
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <div className="profile-container">
      <div className="card">
        <div className="card-body">
          <h1 className="card-title">Your Profile</h1>
          <p className="text-muted">Update your personal information and preferences</p>
          
          {success && (
            <div className="alert alert-success">
              Your profile has been updated successfully!
            </div>
          )}
          
          {errors.general && (
            <div className="alert alert-danger">{errors.general}</div>
          )}
          
          <form onSubmit={handleSubmit}>
            <div className="row mb-4">
              <div className="col-12">
                <h4 className="mb-3">Personal Information</h4>
              </div>
              
              <div className="col-md-6 mb-3">
                <label htmlFor="first_name" className="form-label">First Name</label>
                <input
                  type="text"
                  className={`form-control ${errors.first_name ? 'is-invalid' : ''}`}
                  id="first_name"
                  name="first_name"
                  value={formData.first_name}
                  onChange={handleChange}
                  disabled={loading}
                />
                {errors.first_name && (
                  <div className="invalid-feedback">{errors.first_name}</div>
                )}
              </div>
              
              <div className="col-md-6 mb-3">
                <label htmlFor="last_name" className="form-label">Last Name</label>
                <input
                  type="text"
                  className={`form-control ${errors.last_name ? 'is-invalid' : ''}`}
                  id="last_name"
                  name="last_name"
                  value={formData.last_name}
                  onChange={handleChange}
                  disabled={loading}
                />
                {errors.last_name && (
                  <div className="invalid-feedback">{errors.last_name}</div>
                )}
              </div>
              
              <div className="col-md-6 mb-3">
                <label htmlFor="email" className="form-label">Email</label>
                <input
                  type="email"
                  className={`form-control ${errors.email ? 'is-invalid' : ''}`}
                  id="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  disabled={loading}
                />
                {errors.email && (
                  <div className="invalid-feedback">{errors.email}</div>
                )}
              </div>
            </div>
            
            <div className="row mb-4">
              <div className="col-12">
                <h4 className="mb-3">Physical Information</h4>
              </div>
              
              <div className="col-md-4 mb-3">
                <label htmlFor="profile.age" className="form-label">Age</label>
                <input
                  type="number"
                  className={`form-control ${errors['profile.age'] ? 'is-invalid' : ''}`}
                  id="profile.age"
                  name="profile.age"
                  value={formData.profile.age}
                  onChange={handleChange}
                  disabled={loading}
                />
                {errors['profile.age'] && (
                  <div className="invalid-feedback">{errors['profile.age']}</div>
                )}
              </div>
              
              <div className="col-md-4 mb-3">
                <label htmlFor="profile.height" className="form-label">Height (cm)</label>
                <input
                  type="number"
                  step="0.1"
                  className={`form-control ${errors['profile.height'] ? 'is-invalid' : ''}`}
                  id="profile.height"
                  name="profile.height"
                  value={formData.profile.height}
                  onChange={handleChange}
                  disabled={loading}
                />
                {errors['profile.height'] && (
                  <div className="invalid-feedback">{errors['profile.height']}</div>
                )}
              </div>
              
              <div className="col-md-4 mb-3">
                <label htmlFor="profile.weight" className="form-label">Weight (kg)</label>
                <input
                  type="number"
                  step="0.1"
                  className={`form-control ${errors['profile.weight'] ? 'is-invalid' : ''}`}
                  id="profile.weight"
                  name="profile.weight"
                  value={formData.profile.weight}
                  onChange={handleChange}
                  disabled={loading}
                />
                {errors['profile.weight'] && (
                  <div className="invalid-feedback">{errors['profile.weight']}</div>
                )}
              </div>
              
              <div className="col-md-4 mb-3">
                <label htmlFor="profile.gender" className="form-label">Gender</label>
                <select
                  className={`form-select ${errors['profile.gender'] ? 'is-invalid' : ''}`}
                  id="profile.gender"
                  name="profile.gender"
                  value={formData.profile.gender}
                  onChange={handleChange}
                  disabled={loading}
                >
                  <option value="">Select Gender</option>
                  <option value="male">Male</option>
                  <option value="female">Female</option>
                  <option value="other">Other</option>
                </select>
                {errors['profile.gender'] && (
                  <div className="invalid-feedback">{errors['profile.gender']}</div>
                )}
              </div>
            </div>
            
            <div className="row mb-4">
              <div className="col-12">
                <h4 className="mb-3">Diet & Activity Preferences</h4>
              </div>
              
              <div className="col-md-6 mb-3">
                <label htmlFor="profile.activity_level" className="form-label">Activity Level</label>
                <select
                  className={`form-select ${errors['profile.activity_level'] ? 'is-invalid' : ''}`}
                  id="profile.activity_level"
                  name="profile.activity_level"
                  value={formData.profile.activity_level}
                  onChange={handleChange}
                  disabled={loading}
                >
                  <option value="sedentary">Sedentary (little or no exercise)</option>
                  <option value="light">Lightly Active (light exercise/sports 1-3 days/week)</option>
                  <option value="moderate">Moderately Active (moderate exercise/sports 3-5 days/week)</option>
                  <option value="active">Active (hard exercise/sports 6-7 days a week)</option>
                  <option value="very_active">Very Active (very hard exercise & physical job)</option>
                </select>
                {errors['profile.activity_level'] && (
                  <div className="invalid-feedback">{errors['profile.activity_level']}</div>
                )}
              </div>
              
              <div className="col-md-6 mb-3">
                <label htmlFor="profile.dietary_preference" className="form-label">Dietary Preference</label>
                <select
                  className={`form-select ${errors['profile.dietary_preference'] ? 'is-invalid' : ''}`}
                  id="profile.dietary_preference"
                  name="profile.dietary_preference"
                  value={formData.profile.dietary_preference}
                  onChange={handleChange}
                  disabled={loading}
                >
                  <option value="omnivore">Omnivore (eat everything)</option>
                  <option value="vegetarian">Vegetarian (no meat)</option>
                  <option value="vegan">Vegan (no animal products)</option>
                  <option value="keto">Ketogenic (high fat, low carb)</option>
                  <option value="paleo">Paleo (lean meats, fish, fruits, vegetables, nuts, seeds)</option>
                </select>
                {errors['profile.dietary_preference'] && (
                  <div className="invalid-feedback">{errors['profile.dietary_preference']}</div>
                )}
              </div>
              
              <div className="col-12 mb-3">
                <label htmlFor="profile.allergies" className="form-label">Allergies or Food Restrictions</label>
                <textarea
                  className={`form-control ${errors['profile.allergies'] ? 'is-invalid' : ''}`}
                  id="profile.allergies"
                  name="profile.allergies"
                  rows="2"
                  placeholder="List allergies separated by commas (e.g., peanuts, shellfish, gluten)"
                  value={formData.profile.allergies}
                  onChange={handleChange}
                  disabled={loading}
                ></textarea>
                {errors['profile.allergies'] && (
                  <div className="invalid-feedback">{errors['profile.allergies']}</div>
                )}
              </div>
            </div>
            
            <div className="row mb-4">
              <div className="col-12">
                <h4 className="mb-3">Integration Settings</h4>
              </div>
              
              <div className="col-md-6 mb-3">
                <label htmlFor="profile.fitness_api_id" className="form-label">Fitness Tracker API ID</label>
                <input
                  type="text"
                  className={`form-control ${errors['profile.fitness_api_id'] ? 'is-invalid' : ''}`}
                  id="profile.fitness_api_id"
                  name="profile.fitness_api_id"
                  placeholder="Your ID from your classmate's fitness tracker API"
                  value={formData.profile.fitness_api_id}
                  onChange={handleChange}
                  disabled={loading}
                />
                {errors['profile.fitness_api_id'] && (
                  <div className="invalid-feedback">{errors['profile.fitness_api_id']}</div>
                )}
                <div className="form-text">
                  This ID links to your classmate's Fitness Tracker API
                </div>
              </div>
              
              <div className="col-md-6 mb-3">
                <label htmlFor="profile.location" className="form-label">Default Location</label>
                <input
                  type="text"
                  className={`form-control ${errors['profile.location'] ? 'is-invalid' : ''}`}
                  id="profile.location"
                  name="profile.location"
                  placeholder="e.g., Dublin, Ireland"
                  value={formData.profile.location}
                  onChange={handleChange}
                  disabled={loading}
                />
                {errors['profile.location'] && (
                  <div className="invalid-feedback">{errors['profile.location']}</div>
                )}
                <div className="form-text">
                  Your default location for weather data (can be overridden when generating meal plans)
                </div>
              </div>
            </div>
            
            <div className="d-grid gap-2">
              <button
                type="submit"
                className="btn btn-primary btn-lg"
                disabled={loading}
              >
                {loading ? 'Saving...' : 'Save Profile'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Profile;