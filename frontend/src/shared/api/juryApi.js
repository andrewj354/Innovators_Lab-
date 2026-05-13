import client from './client';

/**
 * Отримати мої призначення для оцінки
 */
export const getMyAssignments = () => {
  return client.get('/jury-assignments/my_assignments/');
};

/**
 * Отримати невиконані завдання
 */
export const getPendingAssignments = () => {
  return client.get('/jury-assignments/pending/');
};

/**
 * Отримати деталі призначення
 * @param {number} assignmentId - ID призначення
 */
export const getAssignmentDetail = (assignmentId) => {
  return client.get(`/jury-assignments/${assignmentId}/`);
};

/**
 * Позначити призначення як оцінене
 * @param {number} assignmentId - ID призначення
 */
export const markAssignmentAsEvaluated = (assignmentId) => {
  return client.post(`/jury-assignments/${assignmentId}/mark_as_evaluated/`);
};

/**
 * Розподілити завдання між журі (Admin only)
 * @param {object} distributionData - {submission_ids, jury_ids, tasks_per_jury}
 */
export const distributeAssignments = (distributionData) => {
  return client.post('/jury-assignments/distribute_tasks/', distributionData);
};

/**
 * Оцінити подачу
 * @param {object} scoreData - дані оцінки
 */
export const createScore = (scoreData) => {
  return client.post('/scores/', scoreData);
};

/**
 * Оновити оцінку
 * @param {number} scoreId - ID оцінки
 * @param {object} scoreData - оновлені дані
 */
export const updateScore = (scoreId, scoreData) => {
  return client.put(`/scores/${scoreId}/`, scoreData);
};

/**
 * Отримати порівняння оцінок для подачи
 * @param {number} scoreId - ID оцінки
 */
export const getScoreComparison = (scoreId) => {
  return client.get(`/scores/${scoreId}/comparison/`);
};
