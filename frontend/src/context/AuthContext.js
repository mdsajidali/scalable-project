import React, { createContext, useState, useEffect, useContext } from 'react';
import axios from 'axios';
import { API_BASE_URL } from '../config';

// Create context
const AuthContext = createContext();

// Custom hook for using auth context
export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
  const [currentUser, setCurrentUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [loading, setLoading] = useState(true);

  // Update auth header for axios requests
  const updateAuthHeader = (newToken) => {
    if (newToken) {
      axios.defaults.headers.common['Authorization'] = `Token ${newToken}`;
    } else {
      delete axios.defaults.headers.common['Authorization'];
    }
  };

  // Login function
  const login = async (username, password) => {
    try {
      const response = await axios.post(`${API_BASE_URL}/api/users/login/`, {
        username,
        password
      });
      
      const { token, user_id, username: user_name } = response.data;
      
      // Save token to localStorage
      localStorage.setItem('token', token);
      
      // Update state
      setToken(token);
      setCurrentUser({
        id: user_id,
        username: user_name
      });
      
      // Update axios header
      updateAuthHeader(token);
      
      return response.data;
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    }
  };

  // Register function
  const testApiConnection = async () => {
  try {
    // Try direct connection to backend
    const response = await axios.get('http://localhost:8000/api/test/');
    console.log('Direct API test result:', response.data);
    alert('API connection successful!');
  } catch (error) {
    console.error('API test error:', error);
    alert('API connection failed!');
  }
  };
  const register = async (userData) => {
    try {
      const response = await axios.post(`${API_BASE_URL}/api/users/register/`, userData);
      
      const { token, user_id, username } = response.data;
      
      // Save token to localStorage
      localStorage.setItem('token', token);
      
      // Update state
      setToken(token);
      setCurrentUser({
        id: user_id,
        username
      });
      
      // Update axios header
      updateAuthHeader(token);
      
      return response.data;
    } catch (error) {
      console.error('Registration error:', error);
      throw error;
    }
  };

  // Logout function
  const logout = async () => {
    try {
      if (token) {
        await axios.post(`${API_BASE_URL}/api/users/logout/`);
      }
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      // Clear token from localStorage
      localStorage.removeItem('token');
      
      // Update state
      setToken(null);
      setCurrentUser(null);
      
      // Remove auth header
      updateAuthHeader(null);
    }
  };

  // Get user profile
  const fetchUserProfile = async () => {
    if (!token) {
      setLoading(false);
      return;
    }
    
    try {
      updateAuthHeader(token);
      
      const response = await axios.get(`${API_BASE_URL}/api/users/profile/`);
      
      setCurrentUser({
        id: response.data.id,
        username: response.data.username,
        email: response.data.email,
        firstName: response.data.first_name,
        lastName: response.data.last_name,
        profile: response.data.profile
      });
    } catch (error) {
      console.error('Error fetching user profile:', error);
      // If there's an authentication error, logout
      if (error.response && (error.response.status === 401 || error.response.status === 403)) {
        logout();
      }
    } finally {
      setLoading(false);
    }
  };

  // Update user profile
  const updateProfile = async (userData) => {
    try {
      const response = await axios.put(`${API_BASE_URL}/api/users/profile/`, userData);
      
      setCurrentUser({
        ...currentUser,
        ...response.data
      });
      
      return response.data;
    } catch (error) {
      console.error('Update profile error:', error);
      throw error;
    }
  };

  // Effect hook to fetch user data on mount or token change
  useEffect(() => {
    if (token) {
      fetchUserProfile();
    } else {
      setLoading(false);
    }
  }, [token]);

  // Set up axios interceptor for token refresh or logout on error
  useEffect(() => {
    // Set initial auth header
    updateAuthHeader(token);
    
    // Add response interceptor
    const interceptor = axios.interceptors.response.use(
      response => response,
      error => {
        // If unauthorized, logout
        if (error.response && (error.response.status === 401 || error.response.status === 403)) {
          logout();
        }
        return Promise.reject(error);
      }
    );
    
    // Clean up interceptor
    return () => axios.interceptors.response.eject(interceptor);
  }, []);

  // Value object to provide to consumers
  const value = {
    currentUser,
    isAuthenticated: !!token,
    loading,
    login,
    register,
    logout,
    updateProfile
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};