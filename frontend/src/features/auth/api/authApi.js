/**
 * Auth API — реєстрація, логін, логаут, refresh.
 * Використовує спільний axios client з shared/api/client.
 */
import client from '../../../shared/api/client';

export const register = async (data) => {
  const response = await client.post('/auth/register', data);
  return response.data;
};

export const login = async (data) => {
  const response = await client.post('/auth/login', data);
  if (response.data.accessToken) {
    localStorage.setItem('accessToken', response.data.accessToken);
  }
  return response.data;
};

export const logout = async () => {
  await client.post('/auth/logout');
  localStorage.removeItem('accessToken');
};

export const refreshToken = async () => {
  const response = await client.post('/auth/token/refresh');
  if (response.data.accessToken) {
    localStorage.setItem('accessToken', response.data.accessToken);
  }
  return response.data;
};
