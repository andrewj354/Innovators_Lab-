const BASE_URL = '/api/jury';

export const getAssignments = async () => {
  const response = await fetch(`${BASE_URL}/assignments/`);
  return response.json();
};

export const getAssignment = async (id) => {
  const response = await fetch(`${BASE_URL}/assignments/${id}/`);
  return response.json();
};

export const submitScore = async (assignmentId, data) => {
  const response = await fetch(`${BASE_URL}/assignments/${assignmentId}/score/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  return response.json();
};