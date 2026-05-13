import client from './client';

/**
 * Отримати список завдань для турніру
 * @param {number} tournamentId - ID турніру
 * @param {string} status - draft|published|closed
 * @param {string} ordering - "-deadline" або "deadline"
 */
export const getTasks = (tournamentId, status = null, ordering = null) => {
  const params = { tournament_id: tournamentId };
  if (status) params.status = status;
  if (ordering) params.ordering = ordering;
  return client.get('/tasks/', { params });
};

/**
 * Отримати деталі завдання
 * @param {number} taskId - ID завдання
 */
export const getTaskDetail = (taskId) => {
  return client.get(`/tasks/${taskId}/`);
};

/**
 * Отримати вимоги завдання
 * @param {number} taskId - ID завдання
 */
export const getTaskRequirements = (taskId) => {
  return client.get(`/tasks/${taskId}/requirements/`);
};

/**
 * Отримати статистику завдання
 * @param {number} taskId - ID завдання
 */
export const getTaskStatistics = (taskId) => {
  return client.get(`/tasks/${taskId}/statistics/`);
};

/**
 * Створити завдання (Admin only)
 * @param {object} taskData - дані завдання
 */
export const createTask = (taskData) => {
  return client.post('/tasks/', taskData);
};

/**
 * Оновити завдання (Admin only)
 * @param {number} taskId - ID завдання
 * @param {object} taskData - оновлені дані
 */
export const updateTask = (taskId, taskData) => {
  return client.put(`/tasks/${taskId}/`, taskData);
};

/**
 * Додати вимогу до завдання (Admin only)
 * @param {number} taskId - ID завдання
 * @param {object} requirementData - {title, is_required}
 */
export const addTaskRequirement = (taskId, requirementData) => {
  return client.post(`/tasks/${taskId}/add_requirement/`, requirementData);
};
