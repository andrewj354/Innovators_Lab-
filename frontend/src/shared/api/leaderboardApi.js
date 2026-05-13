import client from './client';

/**
 * Отримати лідербордом для турніру
 * @param {number} tournamentId - ID турніру
 */
export const getLeaderboard = (tournamentId) => {
  return client.get('/leaderboard/by_tournament/', {
    params: { tournament_id: tournamentId }
  });
};

/**
 * Отримати топ команди турніру
 * @param {number} tournamentId - ID турніру
 * @param {number} limit - кількість команд для повернення
 */
export const getTopTeams = (tournamentId, limit = 10) => {
  return client.get('/leaderboard/top_teams/', {
    params: { tournament_id: tournamentId, limit }
  });
};

/**
 * Пересчитати лідербордом (Admin only)
 * @param {number} tournamentId - ID турніру
 */
export const recalculateLeaderboard = (tournamentId) => {
  return client.post('/leaderboard/recalculate/', {
    tournament_id: tournamentId
  });
};
