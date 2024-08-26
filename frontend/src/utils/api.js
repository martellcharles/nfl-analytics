// API interceptors
// Runs every time the application requests / receives data from the server
import axios from 'axios';

const baseURL = "http://localhost:5000/api"

const api = axios.create({ baseURL });

// runs before every request to the backend
// attaches the authorization header to the request
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;