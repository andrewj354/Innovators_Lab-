/**
 * Auth API — реєстрація, логін, логаут, refresh.
 * Використовує спільний axios client з shared/api/client.
 */
import client from '../../../shared/api/client';

export const register = async (data) => {
  const response = await client.post('/auth/register/', data);
  return response.data;
};

export const login = async (data) => {
  const response = await client.post('/auth/login/', data);
  if (response.data.access) {
    localStorage.setItem('accessToken', response.data.access);
  }
  if (response.data.refresh) {
    localStorage.setItem('refreshToken', response.data.refresh);
  }
  return response.data;
};

export const logout = async () => {
  localStorage.removeItem('accessToken');
  localStorage.removeItem('refreshToken');
  // Optional: call logout endpoint if backend supports it
  // await client.post('/auth/logout');
};

export const refreshToken = async () => {
  const refreshToken = localStorage.getItem('refreshToken');
  if (!refreshToken) {
    throw new Error('No refresh token available');
  }
  const response = await client.post('/auth/refresh/', {
    refresh: refreshToken
  });
  if (response.data.access) {
    localStorage.setItem('accessToken', response.data.access);
  }
  if (response.data.refresh) {
    localStorage.setItem('refreshToken', response.data.refresh);
  }
  return response.data;
};

export const forgotPassword = async (email) => {
  const response = await client.post('/auth/forgot-password/', { email });
  return response.data;
};

export const resetPassword = async (data) => {
  const response = await client.post('/auth/reset-password/', data);
  return response.data;
};

export const getMe = async () => {
  const response = await client.get('/auth/me/');
  return response.data;
};
