import client from './client';

/**
 * Отримати список подач для завдання або команди
 * @param {number} taskId - ID завдання (опціонально)
 * @param {number} teamId - ID команди (опціонально)
 * @param {boolean} isLocked - фільтр за блокуванням (опціонально)
 */
export const getSubmissions = (taskId = null, teamId = null, isLocked = null) => {
  const params = {};
  if (taskId) params.task = taskId;
  if (teamId) params.team_id = teamId;
  if (isLocked !== null) params.is_locked = isLocked;
  return client.get('/submissions/', { params });
};

/**
 * Отримати подачу по ID
 * @param {number} submissionId - ID подачи
 */
export const getSubmissionDetail = (submissionId) => {
  return client.get(`/submissions/${submissionId}/`);
};

/**
 * Отримати подачи команди
 * @param {number} teamId - ID команди
 */
export const getTeamSubmissions = (teamId) => {
  return client.get('/submissions/by_team/', { params: { team_id: teamId } });
};

/**
 * Отримати оцінки для подачи
 * @param {number} submissionId - ID подачи
 */
export const getSubmissionScores = (submissionId) => {
  return client.get(`/submissions/${submissionId}/jury_assignments/`);
};

/**
 * Створити подачу
 * @param {object} submissionData - дані подачи
 */
export const createSubmission = (submissionData) => {
  return client.post('/submissions/', submissionData);
};

/**
 * Оновити подачу
 * @param {number} submissionId - ID подачи
 * @param {object} submissionData - оновлені дані
 */
export const updateSubmission = (submissionId, submissionData) => {
  return client.put(`/submissions/${submissionId}/`, submissionData);
};

/**
 * Заблокувати подачу (Admin only)
 * @param {number} submissionId - ID подачи
 */
export const lockSubmission = (submissionId) => {
  return client.post(`/submissions/${submissionId}/lock/`);
};

/**
 * Розблокувати подачу (Admin only)
 * @param {number} submissionId - ID подачи
 */
export const unlockSubmission = (submissionId) => {
  return client.post(`/submissions/${submissionId}/unlock/`);
};
