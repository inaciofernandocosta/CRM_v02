import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000',
  timeout: 30000, // Aumentando para 30 segundos
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error);
    if (error.code === 'ECONNABORTED') {
      console.error('Request timed out');
    }
    if (error.response) {
      console.error('Response error:', error.response.data);
    }
    return Promise.reject(error);
  }
);

export default api;
