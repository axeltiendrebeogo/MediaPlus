import axios from 'axios';

const BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: BASE_URL,
  headers: { 'Content-Type': 'application/json' },
});

// Attach access token
api.interceptors.request.use(config => {
  const token = localStorage.getItem('mp_access');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// Auto-refresh on 401
let refreshing = false;
let queue = [];

api.interceptors.response.use(
  res => res,
  async err => {
    const original = err.config;
    if (err.response?.status === 401 && !original._retry) {
      if (refreshing) {
        return new Promise((resolve, reject) => {
          queue.push({ resolve, reject, config: original });
        });
      }
      original._retry = true;
      refreshing = true;
      try {
        const refresh = localStorage.getItem('mp_refresh');
        const res = await axios.post(`${BASE_URL}/token/refresh/`, { refresh });
        localStorage.setItem('mp_access', res.data.access);
        queue.forEach(({ resolve, config }) => {
          config.headers.Authorization = `Bearer ${res.data.access}`;
          resolve(api(config));
        });
        queue = [];
        original.headers.Authorization = `Bearer ${res.data.access}`;
        return api(original);
      } catch {
        queue.forEach(({ reject }) => reject(err));
        queue = [];
        localStorage.removeItem('mp_access');
        localStorage.removeItem('mp_refresh');
        window.location.href = '/connexion';
      } finally {
        refreshing = false;
      }
    }
    return Promise.reject(err);
  }
);

export default api;
