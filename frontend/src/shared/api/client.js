import axios from 'axios';


const client = axios.create({
  // Додаємо /api вручну, якщо його немає в env
  baseURL: import.meta.env.VITE_API_URL.endsWith('/api') 
    ? import.meta.env.VITE_API_URL 
    : `${import.meta.env.VITE_API_URL}/api`,
  withCredentials: true,
  headers: { 'Content-Type': 'application/json' },
});

// ─── interceptor: автоматично додає Authorization header ───────────────────
client.interceptors.request.use((config) => {
  const token = localStorage.getItem('accessToken');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// ─── interceptor: при 401 — пробує refresh, повторює запит ─────────────────
let isRefreshing = false;
let failedQueue = [];

const processQueue = (error, token = null) => {
  failedQueue.forEach((prom) =>
    error ? prom.reject(error) : prom.resolve(token)
  );
  failedQueue = [];
};

client.interceptors.response.use(
  (response) => response,
  async (error) => {
    const original = error.config;

    if (error.response?.status === 401 && !original._retry) {
      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject });
        })
          .then((token) => {
            original.headers.Authorization = `Bearer ${token}`;
            return client(original);
          })
          .catch(Promise.reject.bind(Promise));
      }

      original._retry = true;
      isRefreshing = true;

      try {
        const refreshToken = localStorage.getItem('refreshToken');
        const { data } = await client.post('/auth/refresh/', {
          refresh: refreshToken
        });
        localStorage.setItem('accessToken', data.access);
        if (data.refresh) {
          localStorage.setItem('refreshToken', data.refresh);
        }
        client.defaults.headers.Authorization = `Bearer ${data.access}`;
        processQueue(null, data.access);
        return client(original);
      } catch (refreshError) {
        processQueue(refreshError, null);
        localStorage.removeItem('accessToken');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      } finally {
        isRefreshing = false;
      }
    }

    return Promise.reject(error);
  }
);

export default client;
