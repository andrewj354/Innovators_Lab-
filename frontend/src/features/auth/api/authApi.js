/**
 * Auth API — реєстрація, логін, логаут, refresh.
 * Використовує спільний axios client з shared/api/client.
 */
import client from '../../../shared/api/client';

export const register = async (data) => {
  // MOCK: Імітуємо успішну реєстрацію з затримкою
  return new Promise((resolve) => setTimeout(() => resolve({ success: true }), 800));

  // REAL API (закоментовано поки немає бекенду):
  // const response = await client.post('/auth/register', data);
  // return response.data;
};

export const login = async (data) => {
  // MOCK: Імітуємо успішний логін
  return new Promise((resolve) => setTimeout(() => {
    localStorage.setItem('accessToken', 'mock-token-123');
    resolve({ accessToken: 'mock-token-123' });
  }, 800));

  // REAL API:
  // const response = await client.post('/auth/login', data);
  // if (response.data.accessToken) {
  //   localStorage.setItem('accessToken', response.data.accessToken);
  // }
  // return response.data;
};

export const logout = async () => {
  // MOCK:
  localStorage.removeItem('accessToken');

  // REAL API:
  // await client.post('/auth/logout');
  // localStorage.removeItem('accessToken');
};

export const refreshToken = async () => {
  const response = await client.post('/auth/token/refresh');
  if (response.data.accessToken) {
    localStorage.setItem('accessToken', response.data.accessToken);
  }
  return response.data;
};

export const forgotPassword = async (email) => {
  // MOCK: Імітуємо відправку листа
  return new Promise((resolve) => setTimeout(() => resolve({ success: true }), 800));

  // REAL API:
  // const response = await client.post('/auth/forgot-password', { email });
  // return response.data;
};

export const resetPassword = async (data) => {
  // MOCK: Імітуємо зміну паролю
  return new Promise((resolve) => setTimeout(() => resolve({ success: true }), 800));

  // REAL API:
  // const response = await client.post('/auth/reset-password', data);
  // return response.data;
};
