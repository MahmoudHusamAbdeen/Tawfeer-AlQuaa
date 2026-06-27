/**
 * Tawfeer Frontend API Service
 * =============================
 * Replace all AsyncStorage calls with these API functions
 * to connect your React Native app to the Python backend.
 *
 * SETUP:
 * 1. Copy this file to your frontend project: src/services/api.js
 * 2. Install axios: npm install axios
 * 3. Update the BASE_URL below to your server IP address
 * 4. Replace AsyncStorage calls in each screen with the API functions
 */

import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

// ============================================
// CONFIGURATION - Change this to your server IP
// ============================================
// For emulator: use http://10.0.2.2:8000 (Android) or http://localhost:8000 (iOS)
// For physical device: use your computer's local IP (e.g., http://192.168.1.100:8000)
const BASE_URL = 'http://10.0.2.2:8000';

// Create axios instance with default config
const api = axios.create({
  baseURL: BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// ============================================
// REQUEST INTERCEPTOR - Add auth token to requests
// ============================================
api.interceptors.request.use(
  async (config) => {
    const token = await AsyncStorage.getItem('auth_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// ============================================
// RESPONSE INTERCEPTOR - Handle auth errors
// ============================================
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      await AsyncStorage.removeItem('auth_token');
      await AsyncStorage.removeItem('user_data');
    }
    return Promise.reject(error);
  }
);

// ============================================
// AUTHENTICATION APIs
// ============================================

export const registerUser = async (userData) => {
  try {
    const response = await api.post('/api/auth/register', {
      name: userData.name,
      email: userData.email,
      phone: userData.phone,
      password: userData.password,
      type: userData.type || 'Household',
      custom_type: userData.customType,
    });
    await AsyncStorage.setItem('auth_token', response.data.access_token);
    await AsyncStorage.setItem('user_data', JSON.stringify(response.data.user));
    return response.data;
  } catch (error) {
    const message = error.response?.data?.detail || 'Registration failed';
    throw new Error(message);
  }
};

export const loginUser = async (emailOrPhone, password) => {
  try {
    const response = await api.post('/api/auth/login', {
      email_or_phone: emailOrPhone,
      password: password,
    });
    await AsyncStorage.setItem('auth_token', response.data.access_token);
    await AsyncStorage.setItem('user_data', JSON.stringify(response.data.user));
    await AsyncStorage.setItem('user_role', response.data.role);
    return response.data;
  } catch (error) {
    const message = error.response?.data?.detail || 'Login failed';
    throw new Error(message);
  }
};

export const loginDriver = async (username, password) => {
  try {
    const response = await api.post('/api/auth/driver-login', {
      username: username,
      password: password,
    });
    await AsyncStorage.setItem('auth_token', response.data.access_token);
    await AsyncStorage.setItem('user_data', JSON.stringify(response.data.user));
    await AsyncStorage.setItem('user_role', 'driver');
    return response.data;
  } catch (error) {
    const message = error.response?.data?.detail || 'Driver login failed';
    throw new Error(message);
  }
};

export const getCurrentUserData = async () => {
  try {
    const response = await api.get('/api/auth/me');
    return response.data;
  } catch (error) {
    const message = error.response?.data?.detail || 'Failed to get user data';
    throw new Error(message);
  }
};

export const updateProfile = async (profileData) => {
  try {
    const response = await api.put('/api/auth/profile', profileData);
    await AsyncStorage.setItem('user_data', JSON.stringify(response.data));
    return response.data;
  } catch (error) {
    const message = error.response?.data?.detail || 'Profile update failed';
    throw new Error(message);
  }
};

export const logoutUser = async () => {
  await AsyncStorage.removeItem('auth_token');
  await AsyncStorage.removeItem('user_data');
  await AsyncStorage.removeItem('user_role');
};

// ============================================
// AI RECIPE APIs (OpenAI Integration)
// ============================================

export const getRecipeSuggestions = async (ingredients, language = 'en') => {
  try {
    const response = await api.post('/api/ai/recipes', {
      ingredients: ingredients,
      language: language,
    });
    return response.data;
  } catch (error) {
    const message = error.response?.data?.detail || 'Failed to get recipe suggestions';
    throw new Error(message);
  }
};

export const askAIQuestion = async (question, language = 'en') => {
  try {
    const response = await api.post('/api/ai/ask', {
      question: question,
      language: language,
    });
    return response.data;
  } catch (error) {
    const message = error.response?.data?.detail || 'Failed to get AI response';
    throw new Error(message);
  }
};

// ============================================
// DONATION & FOOD REQUEST APIs
// ============================================

export const submitDonation = async (donationData) => {
  try {
    const response = await api.post('/api/donations/donate', donationData);
    return response.data;
  } catch (error) {
    const message = error.response?.data?.detail || 'Donation submission failed';
    throw new Error(message);
  }
};

export const submitFoodRequest = async (requestData) => {
  try {
    const response = await api.post('/api/donations/request', requestData);
    return response.data;
  } catch (error) {
    const message = error.response?.data?.detail || 'Request submission failed';
    throw new Error(message);
  }
};

export const markOrderDone = async (orderId, userEmail) => {
  try {
    const response = await api.post('/api/donations/mark-done', {
      order_id: orderId,
      user_email: userEmail,
    });
    return response.data;
  } catch (error) {
    const message = error.response?.data?.detail || 'Failed to mark order as done';
    throw new Error(message);
  }
};

export const getDonationHistory = async (email) => {
  try {
    const response = await api.get(`/api/donations/history/${email}`);
    return response.data;
  } catch (error) {
    const message = error.response?.data?.detail || 'Failed to get donation history';
    throw new Error(message);
  }
};

export const redeemReward = async (email, pointsCost) => {
  try {
    const response = await api.post('/api/donations/redeem-reward', null, {
      params: { email, points_cost: pointsCost }
    });
    return response.data;
  } catch (error) {
    const message = error.response?.data?.detail || 'Reward redemption failed';
    throw new Error(message);
  }
};

// ============================================
// ADMIN APIs
// ============================================

export const getAdminStats = async () => {
  try {
    const response = await api.get('/api/admin/stats');
    return response.data;
  } catch (error) {
    const message = error.response?.data?.detail || 'Failed to get admin stats';
    throw new Error(message);
  }
};

export const getAllUsers = async () => {
  try {
    const response = await api.get('/api/admin/users');
    return response.data;
  } catch (error) {
    const message = error.response?.data?.detail || 'Failed to get users';
    throw new Error(message);
  }
};

export const getAllOrders = async () => {
  try {
    const response = await api.get('/api/admin/orders');
    return response.data;
  } catch (error) {
    const message = error.response?.data?.detail || 'Failed to get orders';
    throw new Error(message);
  }
};

export const approveOrder = async (orderId, driverName, driverPhone, estimatedTime) => {
  try {
    const response = await api.post('/api/admin/approve-order', {
      order_id: orderId,
      driver_name: driverName,
      driver_phone: driverPhone,
      estimated_time: estimatedTime,
    });
    return response.data;
  } catch (error) {
    const message = error.response?.data?.detail || 'Failed to approve order';
    throw new Error(message);
  }
};

export const rejectOrder = async (orderId) => {
  try {
    const response = await api.post(`/api/admin/reject-order?order_id=${orderId}`);
    return response.data;
  } catch (error) {
    const message = error.response?.data?.detail || 'Failed to reject order';
    throw new Error(message);
  }
};

export const completeOrderByAdmin = async (orderId) => {
  try {
    const response = await api.post(`/api/admin/complete-order?order_id=${orderId}`);
    return response.data;
  } catch (error) {
    const message = error.response?.data?.detail || 'Failed to complete order';
    throw new Error(message);
  }
};

export const deleteUser = async (userEmail) => {
  try {
    const response = await api.delete('/api/admin/user', {
      data: { user_email: userEmail }
    });
    return response.data;
  } catch (error) {
    const message = error.response?.data?.detail || 'Failed to delete user';
    throw new Error(message);
  }
};

export const getAllDrivers = async () => {
  try {
    const response = await api.get('/api/admin/drivers');
    return response.data;
  } catch (error) {
    const message = error.response?.data?.detail || 'Failed to get drivers';
    throw new Error(message);
  }
};

export const createDriver = async (driverData) => {
  try {
    const response = await api.post('/api/admin/drivers', driverData);
    return response.data;
  } catch (error) {
    const message = error.response?.data?.detail || 'Failed to create driver';
    throw new Error(message);
  }
};

export const deleteDriver = async (username) => {
  try {
    const response = await api.delete('/api/admin/drivers', {
      data: { username: username }
    });
    return response.data;
  } catch (error) {
    const message = error.response?.data?.detail || 'Failed to delete driver';
    throw new Error(message);
  }
};

// ============================================
// DRIVER APIs
// ============================================

export const getDriverOrders = async () => {
  try {
    const response = await api.get('/api/driver/orders');
    return response.data;
  } catch (error) {
    const message = error.response?.data?.detail || 'Failed to get driver orders';
    throw new Error(message);
  }
};

export const updateOrderStatus = async (orderId, userEmail, newStatus, options = {}) => {
  try {
    const response = await api.post('/api/driver/update-status', {
      order_id: orderId,
      user_email: userEmail,
      new_status: newStatus,
      delivery_notes: options.deliveryNotes || '',
      driver_location: options.driverLocation || '',
      points_to_award: options.pointsToAward || 0,
    });
    return response.data;
  } catch (error) {
    const message = error.response?.data?.detail || 'Failed to update order status';
    throw new Error(message);
  }
};

export const getDriverStats = async () => {
  try {
    const response = await api.get('/api/driver/stats');
    return response.data;
  } catch (error) {
    const message = error.response?.data?.detail || 'Failed to get driver stats';
    throw new Error(message);
  }
};

// ============================================
// GOVERNMENT APIs
// ============================================

export const getGovernmentStats = async () => {
  try {
    const response = await api.get('/api/government/stats');
    return response.data;
  } catch (error) {
    const message = error.response?.data?.detail || 'Failed to get government stats';
    throw new Error(message);
  }
};

export const getGovernmentChartData = async (viewMode = 'weekly') => {
  try {
    const response = await api.get('/api/government/charts', {
      params: { view_mode: viewMode }
    });
    return response.data;
  } catch (error) {
    const message = error.response?.data?.detail || 'Failed to get chart data';
    throw new Error(message);
  }
};

export const getRecentActivities = async (limit = 10) => {
  try {
    const response = await api.get('/api/government/activities', {
      params: { limit }
    });
    return response.data;
  } catch (error) {
    const message = error.response?.data?.detail || 'Failed to get activities';
    throw new Error(message);
  }
};

export const getTopUsers = async (limit = 10) => {
  try {
    const response = await api.get('/api/government/top-users', {
      params: { limit }
    });
    return response.data;
  } catch (error) {
    const message = error.response?.data?.detail || 'Failed to get top users';
    throw new Error(message);
  }
};

export default api;
