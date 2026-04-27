const BASE_URL = '/api';

export const submitWork = async (taskId, data) => {
  const response = await fetch(`${BASE_URL}/tasks/${taskId}/submit/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  return response.json();
};

export const updateSubmission = async (id, data) => {
  const response = await fetch(`${BASE_URL}/submissions/${id}/`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  return response.json();
};

export const getSubmission = async (id) => {
  const response = await fetch(`${BASE_URL}/submissions/${id}/`);
  return response.json();
};

export const getSubmissions = async (taskId) => {
  const response = await fetch(`${BASE_URL}/tasks/${taskId}/submissions/`);
  return response.json();
};