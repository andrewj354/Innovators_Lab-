import client from '../../../shared/api/client';

/**
 * Отримати список турнірів
 */
export const getTournaments = () => {
  return client.get('/tournaments/');
};

/**
 * Отримати деталі турніру
 * @param {number} tournamentId - ID турніру
 */
export const getTournamentDetail = (tournamentId) => {
  return client.get(`/tournaments/${tournamentId}/`);
};

/**
 * Отримати публічний турнір
 * @param {string} slug - slug турніру
 */
export const getPublicTournament = (slug) => {
  return client.get(`/tournaments/${slug}/public/`);
};

/**
 * Створити турнір (Admin only)
 * @param {object} tournamentData - дані турніру
 */
export const createTournament = (tournamentData) => {
  return client.post('/tournaments/', tournamentData);
};

/**
 * Оновити турнір (Admin only)
 * @param {number} tournamentId - ID турніру
 * @param {object} tournamentData - оновлені дані
 */
export const updateTournament = (tournamentId, tournamentData) => {
  return client.put(`/tournaments/${tournamentId}/`, tournamentData);
};

/**
 * Видалити турнір (Admin only)
 * @param {number} tournamentId - ID турніру
 */
export const deleteTournament = (tournamentId) => {
  return client.delete(`/tournaments/${tournamentId}/`);
};

// ─── Legacy mock exports for backward compatibility ───────────────────────────

export async function getTournament(id) {
  const { data } = await getTournamentDetail(id);
  return data;
}
export async function deleteTournament(id) {
  // return (await client.delete(`/tournaments/${id}`)).data;
  const index = mockTournaments.findIndex((t) => t.id === Number(id));
  if (index === -1) throw new Error('Tournament not found');
  return mockTournaments.splice(index, 1)[0];
}

// Default export для зворотної сумісності
const tournamentApi = {
  getTournaments,
  getTournament,
  createTournament,
  updateTournament,
  deleteTournament,
};

export default tournamentApi;
