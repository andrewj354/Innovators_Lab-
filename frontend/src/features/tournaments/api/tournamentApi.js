/**
 * Tournament API — CRUD для турнірів.
 * Зараз це mock-заглушки з локальними даними.
 * Щоб підключити реальний бекенд — замінити реалізації функцій на client.get/post/put/delete.
 */
// import client from '../../../shared/api/client';  // ← розкоментувати для реального API

// ─── Mock Data ──────────────────────────────────────────────────────────────
const mockTournaments = [
  {
    id: 1,
    game: 'CS2',
    title: 'Весняний Чемпіонат по CS2',
    status: 'активний',
    regStart: '2024-04-01',
    regEnd: '2024-04-15',
    imageUrl: 'https://via.placeholder.com/300x150?text=CS2',
    description: 'Весняний чемпіонат з Counter-Strike 2 для команд з усієї України.',
    teams: [],
  },
  {
    id: 2,
    game: 'League of Legends',
    title: 'Ліга Геймерів League of Legends',
    status: 'майбутній',
    regStart: '2024-05-10',
    regEnd: '2024-05-25',
    imageUrl: 'https://via.placeholder.com/300x150?text=LoL',
    description: 'Ліга Геймерів — серія турнірів для любителів та професіоналів.',
    teams: [],
  },
  {
    id: 3,
    game: 'Dota 2',
    title: 'Кубок України Dota 2',
    status: 'завершений',
    regStart: '2024-02-15',
    regEnd: '2024-02-28',
    imageUrl: 'https://via.placeholder.com/300x150?text=Dota2',
    description: 'Кубок України з Dota 2.',
    teams: [],
  },
  {
    id: 4,
    game: 'VALORANT',
    title: 'Відкритий Турнір по Valorant',
    status: 'активний',
    regStart: '2024-03-20',
    regEnd: '2024-04-10',
    imageUrl: 'https://via.placeholder.com/300x150?text=Valorant',
    description: 'Відкритий турнір для всіх рівнів.',
    teams: [],
  },
  {
    id: 5,
    game: 'FORTNITE',
    title: 'Фінал Сезону Fortnite',
    status: 'майбутній',
    regStart: '2024-06-05',
    regEnd: '2024-06-20',
    imageUrl: 'https://via.placeholder.com/300x150?text=Fortnite',
    description: 'Фінальний турнір сезону з Fortnite.',
    teams: [],
  },
];

// ─── API Functions (mock) ───────────────────────────────────────────────────

/** Отримати список всіх турнірів */
export async function getTournaments() {
  // return (await client.get('/tournaments')).data;
  return [...mockTournaments];
}

/** Отримати один турнір по ID */
export async function getTournament(id) {
  // return (await client.get(`/tournaments/${id}`)).data;
  const tournament = mockTournaments.find((t) => t.id === Number(id));
  if (!tournament) throw new Error('Tournament not found');
  return { ...tournament };
}

/** Створити новий турнір */
export async function createTournament(data) {
  // return (await client.post('/tournaments', data)).data;
  const newTournament = { ...data, id: Date.now() };
  mockTournaments.push(newTournament);
  return newTournament;
}

/** Оновити турнір */
export async function updateTournament(id, data) {
  // return (await client.put(`/tournaments/${id}`, data)).data;
  const index = mockTournaments.findIndex((t) => t.id === Number(id));
  if (index === -1) throw new Error('Tournament not found');
  mockTournaments[index] = { ...mockTournaments[index], ...data };
  return mockTournaments[index];
}

/** Видалити турнір */
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
