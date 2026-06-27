/**
 * Tawfeer Frontend - API Service
 * All backend API calls in one place
 * Import from any screen: import { authApi, aiApi, donationApi } from '../apiService';
 */

import api from './api';

// ==================== AUTH ====================

export const authApi = {
  login: (email, password) => api.post('/auth/login', { email, password }),
  signup: (data) => api.post('/auth/signup', data),
  getProfile: () => api.get('/auth/profile'),
  updateProfile: (data) => api.put('/auth/profile', data),
  changePassword: (data) => api.post('/auth/change-password', data),
  driverLogin: (username, password) => api.post('/auth/driver-login', { username, password }),
  adminLogin: (username, password) => api.post('/auth/admin-login', { username, password }),
};

// ==================== AI ====================

export const aiApi = {
  generateRecipe: (data) => api.post('/ai/generate-recipe', data),
  askQuestion: (question, context) => api.post('/ai/ask', { question, context }),
  getSubstitutes: (ingredient, context) => api.post('/ai/substitute', { ingredient, recipe_context: context }),
  generateMealPlan: (data) => api.post('/ai/generate-meal-plan', data),
  modifyRecipe: (recipeId, modifications) => api.post('/ai/modify-recipe', { recipe_id: recipeId, modifications }),
};

// ==================== DONATIONS ====================

export const donationApi = {
  create: (data) => api.post('/donations', data),
  getAll: (params) => api.get('/donations', { params }),
  getById: (id) => api.get(`/donations/${id}`),
  update: (id, data) => api.put(`/donations/${id}`, data),
  delete: (id) => api.delete(`/donations/${id}`),
  getUserDonations: () => api.get('/donations/my-donations'),
};

// ==================== FOOD REQUESTS ====================

export const foodRequestApi = {
  create: (data) => api.post('/food-requests', data),
  getAll: (params) => api.get('/food-requests', { params }),
  getById: (id) => api.get(`/food-requests/${id}`),
  getUserRequests: () => api.get('/food-requests/my-requests'),
};

// ==================== RECIPES ====================

export const recipeApi = {
  getAll: (params) => api.get('/recipes', { params }),
  get: (id) => api.get(`/recipes/${id}`),
  create: (data) => api.post('/recipes', data),
  update: (id, data) => api.put(`/recipes/${id}`, data),
  delete: (id) => api.delete(`/recipes/${id}`),
  search: (query) => api.get('/recipes/search', { params: { query } }),
  getByCategory: (cat) => api.get(`/recipes/category/${cat}`),
  getCategories: () => api.get('/recipes/categories'),
  toggleFavorite: (recipeId) => api.post('/recipes/favorites/toggle', { recipe_id: recipeId }),
  getFavorites: () => api.get('/recipes/favorites'),
};

// ==================== SHOPPING LISTS ====================

export const shoppingListApi = {
  getAll: () => api.get('/shopping-lists'),
  get: (id) => api.get(`/shopping-lists/${id}`),
  create: (data) => api.post('/shopping-lists', data),
  update: (id, data) => api.put(`/shopping-lists/${id}`, data),
  delete: (id) => api.delete(`/shopping-lists/${id}`),
  addItem: (listId, item) => api.post(`/shopping-lists/${listId}/items`, item),
  updateItem: (listId, itemId, data) => api.put(`/shopping-lists/${listId}/items/${itemId}`, data),
  deleteItem: (listId, itemId) => api.delete(`/shopping-lists/${listId}/items/${itemId}`),
  fromRecipe: (recipeId, name) => api.post('/shopping-lists/from-recipe', { recipe_id: recipeId, list_name: name }),
};

// ==================== MEAL PLANS ====================

export const mealPlanApi = {
  getAll: () => api.get('/meal-plans'),
  get: (id) => api.get(`/meal-plans/${id}`),
  getCurrentWeek: () => api.get('/meal-plans/current-week'),
  create: (data) => api.post('/meal-plans', data),
  update: (id, data) => api.put(`/meal-plans/${id}`, data),
  delete: (id) => api.delete(`/meal-plans/${id}`),
  addMeal: (planId, date, data) => api.post(`/meal-plans/${planId}/days/${date}/meals`, data),
  removeMeal: (planId, date, mealId) => api.delete(`/meal-plans/${planId}/days/${date}/meals/${mealId}`),
};

// ==================== ADMIN ====================

export const adminApi = {
  getStats: () => api.get('/admin/stats'),
  getUsers: () => api.get('/admin/users'),
  getOrders: () => api.get('/admin/orders'),
  approveOrder: (id, data) => api.put(`/admin/orders/${id}/approve`, data),
  completeOrder: (id) => api.put(`/admin/orders/${id}/complete`),
  rejectOrder: (id) => api.put(`/admin/orders/${id}/reject`),
  addDriver: (data) => api.post('/admin/drivers', data),
  getDrivers: () => api.get('/admin/drivers'),
  deleteDriver: (id) => api.delete(`/admin/drivers/${id}`),
};

// ==================== DRIVER ====================

export const driverApi = {
  getOrders: () => api.get('/driver/orders'),
  updateOrderStatus: (id, data) => api.put(`/driver/orders/${id}/status`, data),
  awardPoints: (userId, points) => api.post('/driver/award-points', { user_id: userId, points }),
};

// ==================== GOVERNMENT ====================

export const governmentApi = {
  getStats: () => api.get('/government/stats'),
  getDonations: (params) => api.get('/government/donations', { params }),
  getUserGrowth: (params) => api.get('/government/user-growth', { params }),
  getEnvironmentalImpact: () => api.get('/government/environmental-impact'),
  getRecentActivities: () => api.get('/government/recent-activities'),
};
