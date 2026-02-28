import axios from 'axios';

// Default to the API version root in local dev so endpoints like
// `api.post('/vitals')` resolve to `http://localhost:8000/api/v1/vitals`.
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to request headers if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('authToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  // debug logging when in development mode
  if (import.meta.env.DEV) {
    console.debug('[API] request', config.method, config.url, config.data || config.params);
  }
  return config;
});

// log responses/errors for easier debugging
api.interceptors.response.use(
  (response) => {
    if (import.meta.env.DEV) {
      console.debug('[API] response', response.status, response.config.url, response.data);
    }
    return response;
  },
  (error) => {
    if (import.meta.env.DEV) {
      console.error('[API] error', error);
    }
    return Promise.reject(error);
  }
);

// Auth Service
// NOTE: we intentionally avoid hardcoding the `/api/v1` prefix here so that
// the value of VITE_API_URL can either include or omit it without causing a
// double path issue.  The default baseURL is `http://localhost:8000` but the
// .env may set `http://localhost:8000/api/v1` (see .env.example), therefore
// every endpoint below starts at the version root relative to the base.
export const authService = {
  signup: (name, email, password) =>
    api.post('/auth/signup', { name, email, password }),
  login: (email, password) =>
    api.post('/auth/login', { email, password }),
  getCurrentUser: () =>
    api.get('/auth/me'),
};

// Vitals Service
export const vitalsService = {
  recordVitals: (heartRate, spO2, duration) =>
    api.post('/vitals', { heart_rate: heartRate, spO2, duration }),
  listVitals: (period = 'week') =>
    api.get(`/vitals/`, { params: { period } }),
  getLatestVitals: () =>
    api.get('/vitals/latest'),
};

// Users Service
export const usersService = {
  // fetch the authenticated user's profile
  getProfile: () => api.get('/users/me'),
  updateProfile: (data) => api.patch('/users/me', data),
  changePassword: (oldPassword, newPassword) =>
    api.post('/users/me/password', { old_password: oldPassword, new_password: newPassword }),
  deleteAccount: () => api.delete('/users/me'),

  // administrative / debugging endpoints
  listUsers: () => api.get('/users/'),
};

export default api;
