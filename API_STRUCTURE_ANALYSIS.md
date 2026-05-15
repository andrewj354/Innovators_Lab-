# Comprehensive Backend API Structure Analysis

**Date:** May 15, 2026  
**Scope:** User Service, Task Service, Tournament Service, API Gateway  
**Status:** Based on actual code review of views.py, urls.py, serializers.py

---

## 📋 TABLE OF CONTENTS

1. [API Gateway Architecture](#api-gateway-architecture)
2. [User Service Endpoints](#user-service-endpoints)
3. [Task Service Endpoints](#task-service-endpoints)
4. [Tournament Service Endpoints](#tournament-service-endpoints)
5. [Authentication Flow](#authentication-flow)
6. [Dashboard Data Flow](#dashboard-data-flow)
7. [Frontend Integration Guide](#frontend-integration-guide)
8. [Implementation Status](#implementation-status)

---

## 🔄 API Gateway Architecture

**Location:** `api-gateway/apps/gateway/views.py`  
**Port:** 8000  
**Type:** Reverse proxy with service routing

### Gateway Service Routing Logic:

```
/api/auth/*          → user-service (8001)
/api/users/*         → user-service (8001)
/api/teams/*         → user-service (8001)
/api/tasks/*         → task-service (8002)
/api/submissions/*   → task-service (8002)
/api/jury-assignments/* → rank-service (NOT IMPLEMENTED)
/api/jury/*          → rank-service (NOT IMPLEMENTED)
/api/scores/*        → rank-service (NOT IMPLEMENTED)
/api/leaderboard/*   → rank-service (NOT IMPLEMENTED)
/api/tournaments/*   → tournament-service (8003)
/api/tournament-teams/* → tournament-service (8003)
/api/tournament-rounds/* → tournament-service (8003)
```

### Gateway Features:
- ✅ Forwards Authorization headers
- ✅ Supports JSON/form data
- ✅ Handles query parameters
- ✅ Timeout: 30 seconds per request
- ✅ Error handling for service unavailability

---

## 👤 USER SERVICE ENDPOINTS

**Service:** User Service  
**Port:** 8001  
**Base URLs:** `/api/auth/`, `/api/users/`

### Authentication Endpoints (`/api/auth/*`)

| HTTP | Endpoint | Purpose | Accepts | Returns | Auth Required | Status |
|------|----------|---------|---------|---------|---------------|--------|
| POST | `/api/auth/register/` | Register new user | `{email, username, first_name, last_name, password, password_confirm}` | `{id, email, username, first_name, last_name, message}` | ❌ No | ✅ IMPLEMENTED |
| POST | `/api/auth/login/` | Authenticate user & get tokens | `{email, password}` | `{access, refresh, user: {id, email, username, first_name, last_name, two_fa_enabled}}` | ❌ No | ✅ IMPLEMENTED |
| POST | `/api/auth/refresh/` | Refresh JWT token | `{refresh}` or `{refresh_token}` or `{token}` | `{access}` | ❌ No | ✅ IMPLEMENTED |
| GET | `/api/auth/me/` | Get current user profile | - | `{id, email, username, first_name, last_name, is_active, date_joined, profile: {phone, address, date_of_birth}}` | ✅ YES | ✅ IMPLEMENTED |
| POST | `/api/auth/forgot-password/` | Request password reset | `{email}` | `{message, token}` | ❌ No | ✅ IMPLEMENTED |
| POST | `/api/auth/reset-password/` | Reset password with token | `{token, new_password}` | `{message}` | ❌ No | ✅ IMPLEMENTED |
| POST | `/api/auth/2fa/enable/` | Generate 2FA secret | - | `{secret, qr_code_uri, message}` | ✅ YES | ✅ IMPLEMENTED |
| POST | `/api/auth/2fa/verify/` | Verify & enable 2FA | `{code, secret}` | `{message, two_fa_enabled}` | ✅ YES | ✅ IMPLEMENTED |
| POST | `/api/auth/2fa/verify-login/` | Verify 2FA during login | `{code}` | `{message, verified}` | ✅ YES | ✅ IMPLEMENTED |
| POST | `/api/auth/2fa/disable/` | Disable 2FA | - | `{message, two_fa_enabled}` | ✅ YES | ✅ IMPLEMENTED |

### User Profile Endpoints (`/api/users/*`)

| HTTP | Endpoint | Purpose | Accepts | Returns | Auth Required | Status |
|------|----------|---------|---------|---------|---------------|--------|
| GET | `/api/users/profile/` | Get user profile | - | `{id, email, username, first_name, last_name, is_active, date_joined, profile: {phone, address, date_of_birth}}` | ✅ YES | ✅ IMPLEMENTED |
| PATCH/PUT | `/api/users/profile/update/` | Update user profile | `{phone, address, date_of_birth}` | `{phone, address, date_of_birth}` | ✅ YES | ✅ IMPLEMENTED |

### User Service Serializers:

**UserRegistrationSerializer** (Write):
```json
{
  "email": "user@example.com",
  "username": "username",
  "first_name": "John",
  "last_name": "Doe",
  "password": "securepass123",
  "password_confirm": "securepass123"
}
```

**UserWithProfileSerializer** (Read):
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "username",
  "first_name": "John",
  "last_name": "Doe",
  "is_active": true,
  "date_joined": "2026-01-15T10:30:00Z",
  "profile": {
    "phone": "+380123456789",
    "address": "123 Main St",
    "date_of_birth": "1990-05-15"
  }
}
```

---

## 📝 TASK SERVICE ENDPOINTS

**Service:** Task Service  
**Port:** 8002  
**Base URLs:** `/api/tasks/`, `/api/submissions/`

### Task Endpoints (`/api/tasks/*`)

| HTTP | Endpoint | Purpose | Query Params | Accepts | Returns | Auth Required | Status |
|------|----------|---------|--------------|---------|---------|---------------|--------|
| GET | `/api/tasks/` | List all tasks (paginated) | `page=1&page_size=20&tournament_id=X&status=X&difficulty=X&search=X` | - | `{count, next, previous, results: []}` | ✅ YES | ✅ IMPLEMENTED |
| GET | `/api/tasks/{id}/` | Get task details | - | - | `{id, tournament_id, title, description, difficulty, status, time_limit, memory_limit, points, requirements: [...], created_at, updated_at}` | ✅ YES | ✅ IMPLEMENTED |
| POST | `/api/tasks/` | Create new task | - | `{tournament_id, title, description, difficulty, status, time_limit, memory_limit, points}` | `{id, tournament_id, title, ...}` (full object) | ✅ YES | ✅ IMPLEMENTED |
| PUT | `/api/tasks/{id}/` | Update task | - | `{tournament_id, title, description, difficulty, status, time_limit, memory_limit, points}` | Updated task object | ✅ YES | ✅ IMPLEMENTED |
| PATCH | `/api/tasks/{id}/` | Partial update task | - | Any task fields | Updated task object | ✅ YES | ✅ IMPLEMENTED |
| DELETE | `/api/tasks/{id}/` | Delete task | - | - | 204 No Content | ✅ YES | ✅ IMPLEMENTED |
| GET | `/api/tasks/{id}/requirements/` | Get task test cases | - | - | `[{id, input_data, expected_output, is_sample, created_at}, ...]` | ✅ YES | ✅ IMPLEMENTED |
| POST | `/api/tasks/{id}/add_requirement/` | Add test case to task | - | `{input_data, expected_output, is_sample}` | `{id, input_data, expected_output, is_sample, created_at}` | ✅ YES | ✅ IMPLEMENTED |
| GET | `/api/tasks/{id}/statistics/` | Get task stats | - | - | `{total_submissions, accepted_submissions, average_score, success_rate}` | ✅ YES | ✅ IMPLEMENTED |

### Submission Endpoints (`/api/submissions/*`)

| HTTP | Endpoint | Purpose | Query Params | Accepts | Returns | Auth Required | Status |
|------|----------|---------|--------------|---------|---------|---------------|--------|
| GET | `/api/submissions/` | List submissions (paginated) | `page=1&page_size=20&task_id=X&team_id=X&status=X` | - | `{count, next, previous, results: []}` | ✅ YES | ✅ IMPLEMENTED |
| GET | `/api/submissions/{id}/` | Get submission details | - | - | `{id, task_id, team_id, code, language, status, passed_tests, total_tests, score, is_locked, submitted_at, evaluated_at}` | ✅ YES | ✅ IMPLEMENTED |
| POST | `/api/submissions/` | Create new submission | - | `{task_id, code, language}` | Submission object | ✅ YES | ✅ IMPLEMENTED |
| PUT | `/api/submissions/{id}/` | Update submission | - | `{code, language, status}` | Updated submission | ✅ YES | ✅ IMPLEMENTED |
| PATCH | `/api/submissions/{id}/` | Partial update | - | Any submission fields | Updated submission | ✅ YES | ✅ IMPLEMENTED |
| DELETE | `/api/submissions/{id}/` | Delete submission | - | - | 204 No Content | ✅ YES | ✅ IMPLEMENTED |
| GET | `/api/submissions/by_team/?team_id=X` | Get team submissions | `team_id=X&page=1&page_size=20` | - | `{count, next, previous, results: []}` | ✅ YES | ✅ IMPLEMENTED |
| POST | `/api/submissions/{id}/lock/` | Lock submission | - | - | Submission object | ✅ YES | ✅ IMPLEMENTED |
| POST | `/api/submissions/{id}/unlock/` | Unlock submission | - | - | Submission object | ✅ YES | ✅ IMPLEMENTED |

### Task Service Serializers:

**TaskDetailSerializer** (Read):
```json
{
  "id": 1,
  "tournament_id": 5,
  "title": "Fibonacci Sequence",
  "description": "Calculate nth Fibonacci number",
  "difficulty": "medium",
  "status": "active",
  "time_limit": 2000,
  "memory_limit": 256,
  "points": 100,
  "requirements": [
    {
      "id": 1,
      "input_data": "5",
      "expected_output": "5",
      "is_sample": true,
      "created_at": "2026-01-15T10:30:00Z"
    }
  ],
  "created_at": "2026-01-15T10:30:00Z",
  "updated_at": "2026-01-15T10:30:00Z"
}
```

**SubmissionDetailSerializer** (Read):
```json
{
  "id": 1,
  "task_id": 1,
  "team_id": 5,
  "code": "def fib(n):\n    ...",
  "language": "python",
  "status": "accepted",
  "passed_tests": 10,
  "total_tests": 10,
  "score": 100,
  "is_locked": false,
  "submitted_at": "2026-01-15T10:30:00Z",
  "evaluated_at": "2026-01-15T10:35:00Z"
}
```

---

## 🏆 TOURNAMENT SERVICE ENDPOINTS

**Service:** Tournament Service  
**Port:** 8003  
**Base URL:** `/api/`

### Tournament Endpoints (`/api/tournaments/*`)

| HTTP | Endpoint | Purpose | Query Params | Accepts | Returns | Auth Required | Status |
|------|----------|---------|--------------|---------|---------|---------------|--------|
| GET | `/api/tournaments/` | List all tournaments | `page=1&page_size=20&status=X&created_by=X&ordering=-created_at` | - | `{count, next, previous, results: []}` | ✅ YES | ✅ IMPLEMENTED |
| GET | `/api/tournaments/{id}/` | Get tournament details | - | - | Full tournament object with teams & tasks | ✅ YES | ✅ IMPLEMENTED |
| POST | `/api/tournaments/` | Create tournament | - | `{title, description, reg_start, reg_end, max_teams, status}` | Created tournament object | ✅ YES | ✅ IMPLEMENTED |
| PUT | `/api/tournaments/{id}/` | Update tournament | - | `{title, description, reg_start, reg_end, max_teams, status}` | Updated tournament | ✅ YES | ✅ IMPLEMENTED |
| PATCH | `/api/tournaments/{id}/` | Partial update | - | Any tournament fields | Updated tournament | ✅ YES | ✅ IMPLEMENTED |
| DELETE | `/api/tournaments/{id}/` | Delete tournament | - | - | 204 No Content | ✅ YES | ✅ IMPLEMENTED |
| GET | `/api/tournaments/{id}/teams/` | Get tournament teams | - | - | `[{id, tournament, name, captain_name, captain_email, city, contact, registered_at, members_count}, ...]` | ✅ YES | ✅ IMPLEMENTED |
| GET | `/api/tournaments/{id}/tasks/` | Get tournament tasks | - | - | `[{id, tournament, title, description, status, ...}, ...]` | ✅ YES | ✅ IMPLEMENTED |
| GET | `/api/tournaments/{id}/statistics/` | Get tournament stats | - | - | `{teams_count, max_teams, tasks_count, is_registration_open, can_accept_teams, status}` | ✅ YES | ✅ IMPLEMENTED |

### Team Endpoints (`/api/teams/*`)

| HTTP | Endpoint | Purpose | Query Params | Accepts | Returns | Auth Required | Status |
|------|----------|---------|--------------|---------|---------|---------------|--------|
| GET | `/api/teams/` | List all teams | `page=1&page_size=20&tournament=X&search=X` | - | `{count, next, previous, results: []}` | ✅ YES | ✅ IMPLEMENTED |
| GET | `/api/teams/{id}/` | Get team details | - | - | `{id, tournament, name, captain_name, captain_email, city, contact, registered_at, members: [...], members_count}` | ✅ YES | ✅ IMPLEMENTED |
| POST | `/api/teams/` | Create team | - | `{tournament, name, captain_name, captain_email, city, contact}` | Created team object | ✅ YES | ✅ IMPLEMENTED |
| PUT | `/api/teams/{id}/` | Update team | - | `{tournament, name, captain_name, captain_email, city, contact}` | Updated team | ✅ YES | ✅ IMPLEMENTED |
| PATCH | `/api/teams/{id}/` | Partial update | - | Any team fields | Updated team | ✅ YES | ✅ IMPLEMENTED |
| DELETE | `/api/teams/{id}/` | Delete team | - | - | 204 No Content | ✅ YES | ✅ IMPLEMENTED |
| GET | `/api/teams/{id}/members/` | Get team members | - | - | `[{id, full_name, email}, ...]` | ✅ YES | ✅ IMPLEMENTED |
| POST | `/api/teams/{id}/members/` | Add team member | - | `{full_name, email}` | Created member object | ✅ YES | ✅ IMPLEMENTED |
| GET | `/api/teams/{id}/statistics/` | Get team stats | - | - | `{name, captain, city, members_count, tournament_title, registered_at}` | ✅ YES | ✅ IMPLEMENTED |

### Team Member Endpoints (`/api/team-members/*`)

| HTTP | Endpoint | Purpose | Query Params | Accepts | Returns | Auth Required | Status |
|------|----------|---------|--------------|---------|---------|---------------|--------|
| GET | `/api/team-members/` | List team members | `page=1&page_size=20&team=X&search=X` | - | `{count, next, previous, results: []}` | ✅ YES | ✅ IMPLEMENTED |
| GET | `/api/team-members/{id}/` | Get member details | - | - | `{id, full_name, email}` | ✅ YES | ✅ IMPLEMENTED |
| POST | `/api/team-members/` | Create member | - | `{full_name, email}` | Created member object | ✅ YES | ✅ IMPLEMENTED |
| PUT | `/api/team-members/{id}/` | Update member | - | `{full_name, email}` | Updated member | ✅ YES | ✅ IMPLEMENTED |
| PATCH | `/api/team-members/{id}/` | Partial update | - | Any member fields | Updated member | ✅ YES | ✅ IMPLEMENTED |
| DELETE | `/api/team-members/{id}/` | Delete member | - | - | 204 No Content | ✅ YES | ✅ IMPLEMENTED |

### Tournament Tasks Endpoints (`/api/tasks/*`) - In Tournament Service Context

| HTTP | Endpoint | Purpose | Query Params | Accepts | Returns | Auth Required | Status |
|------|----------|---------|--------------|---------|---------|---------------|--------|
| GET | `/api/tasks/` | List tournament tasks | `page=1&page_size=20&tournament=X&status=X&ordering=start_time` | - | `{count, next, previous, results: []}` | ✅ YES | ✅ IMPLEMENTED |
| GET | `/api/tasks/{id}/` | Get task details | - | - | Full task object with requirements | ✅ YES | ✅ IMPLEMENTED |
| POST | `/api/tasks/` | Create task | - | `{tournament, title, description, tech_requirements, start_time, deadline, status}` | Created task object | ✅ YES | ✅ IMPLEMENTED |
| PUT | `/api/tasks/{id}/` | Update task | - | `{tournament, title, description, tech_requirements, start_time, deadline, status}` | Updated task | ✅ YES | ✅ IMPLEMENTED |
| PATCH | `/api/tasks/{id}/` | Partial update | - | Any task fields | Updated task | ✅ YES | ✅ IMPLEMENTED |
| DELETE | `/api/tasks/{id}/` | Delete task | - | - | 204 No Content | ✅ YES | ✅ IMPLEMENTED |
| GET | `/api/tasks/{id}/requirements/` | Get task requirements | - | - | `[{id, title, is_required}, ...]` | ✅ YES | ✅ IMPLEMENTED |
| POST | `/api/tasks/{id}/requirements/` | Add requirement | - | `{title, is_required}` | Created requirement object | ✅ YES | ✅ IMPLEMENTED |
| GET | `/api/tasks/{id}/statistics/` | Get task stats | - | - | `{title, tournament, is_active, submissions_count, requirements_count, deadline}` | ✅ YES | ✅ IMPLEMENTED |

### Tournament Service Serializers:

**TournamentDetailSerializer** (Read):
```json
{
  "id": 1,
  "created_by": {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com",
    "name": "Admin User",
    "role": "admin",
    "created_at": "2026-01-01T00:00:00Z"
  },
  "title": "2026 Winter Programming Tournament",
  "description": "Annual programming competition",
  "reg_start": "2026-02-01T00:00:00Z",
  "reg_end": "2026-02-15T23:59:59Z",
  "max_teams": 50,
  "status": "upcoming",
  "created_at": "2026-01-15T10:30:00Z",
  "teams": [
    {
      "id": 1,
      "tournament": 1,
      "name": "Python Coders",
      "captain_name": "John Doe",
      "captain_email": "john@example.com",
      "city": "Kyiv",
      "contact": "+380123456789",
      "registered_at": "2026-02-10T10:00:00Z",
      "members_count": 4
    }
  ],
  "tasks": [
    {
      "id": 1,
      "tournament": 1,
      "created_by": 1,
      "title": "Fibonacci",
      "description": "Calculate nth Fibonacci number",
      "tech_requirements": "Python",
      "start_time": "2026-03-01T10:00:00Z",
      "deadline": "2026-03-01T12:00:00Z",
      "status": "active"
    }
  ]
}
```

---

## 🔐 Authentication Flow

### Login Flow (Detailed):

```
1. User submits credentials → POST /api/auth/login/
   INPUT: { email, password }
   
2. Server authenticates user
   OUTPUT: {
     access: "eyJ0eXAiOiJKV1QiLCJhbGc...",
     refresh: "eyJ0eXAiOiJKV1QiLCJhbGc...",
     user: {
       id: 1,
       email: "user@example.com",
       username: "username",
       first_name: "John",
       last_name: "Doe",
       two_fa_enabled: false
     }
   }

3. If 2FA enabled:
   - Server returns 2FA verification required
   - Frontend presents 2FA code input
   - POST /api/auth/2fa/verify-login/ with code
   - Server returns { message, verified }

4. Store tokens in localStorage:
   localStorage.setItem('access_token', access_token)
   localStorage.setItem('refresh_token', refresh_token)
   localStorage.setItem('user', JSON.stringify(user))
```

### JWT Token Structure:

**Access Token:** Short-lived JWT (typically 15-60 minutes)
- Contains user ID and permissions
- Included in `Authorization: Bearer {token}` header

**Refresh Token:** Long-lived JWT (typically 7-30 days)
- Used to obtain new access tokens
- POST to `/api/auth/refresh/` with `{refresh}` body

### Token Refresh Flow:

```
1. When access token expires (401 Unauthorized response):
   POST /api/auth/refresh/
   INPUT: { refresh: refreshToken }
   
2. Server validates refresh token and issues new access token
   OUTPUT: { access: newAccessToken }
   
3. Update localStorage with new access token
   localStorage.setItem('access_token', newAccessToken)
   
4. Retry original request with new access token
```

### 2FA Setup Flow:

```
1. User clicks "Enable 2FA"
   POST /api/auth/2fa/enable/
   OUTPUT: {
     secret: "JBSWY3DPEBLW64TMMQ======",
     qr_code_uri: "otpauth://totp/...",
     message: "Scan this QR code with your authenticator app"
   }

2. Frontend displays QR code (use qr-code library)
   User scans with authenticator app (Google Authenticator, Authy, etc.)

3. User enters 6-digit code from app
   POST /api/auth/2fa/verify/
   INPUT: { code: "123456", secret: "JBSWY3DPEBLW64TMMQ======" }
   OUTPUT: { message: "2FA enabled successfully", two_fa_enabled: true }

4. 2FA now enabled - user must verify code on login
```

### Logout Flow:

```
1. User clicks logout
   - Clear localStorage:
     localStorage.removeItem('access_token')
     localStorage.removeItem('refresh_token')
     localStorage.removeItem('user')
   - Clear AuthContext
   - Redirect to login page
   
Note: No API call required for logout
(Tokens simply expire on client side)
```

---

## 📊 Dashboard Data Endpoints

### What Frontend Should Call After Login:

```javascript
// 1. Get current user profile (already done in me_view)
GET /api/auth/me/

// 2. Get user's dashboard data:
GET /api/tournaments/          // List all tournaments
GET /api/teams/?tournament=X   // Teams user is in
GET /api/submissions/          // User's submissions
GET /api/tasks/                // Available tasks

// 3. Optional - Get specific tournament data:
GET /api/tournaments/{id}/     // Full tournament details
GET /api/tournaments/{id}/statistics/  // Tournament stats
```

### Dashboard Component Data Mapping:

| Dashboard Widget | API Endpoint | Response Field | Display |
|------------------|-------------|-----------------|---------|
| Welcome message | `/api/auth/me/` | `first_name`, `last_name` | "Welcome, John Doe" |
| User email | `/api/auth/me/` | `email` | user@example.com |
| Active tournaments | `/api/tournaments/?status=active` | `results` | List of tournaments |
| My teams | `/api/teams/` | `results` | User's teams |
| My submissions | `/api/submissions/?team_id=X` | `results` | Recent submissions |
| Tournament stats | `/api/tournaments/{id}/statistics/` | `teams_count`, `tasks_count` | Tournament info |
| Leaderboard | ❌ NOT IMPLEMENTED | - | - |

### Dashboard Data Flow Example:

```
1. User logs in → gets access_token
2. AuthContext stores token and user data
3. DashboardPage mounted:
   - Call /api/auth/me/ → get full user profile
   - Call /api/tournaments/ → get all tournaments
   - Call /api/teams/ → get user's teams
   - Call /api/submissions/ → get user's submissions
4. Render dashboard with fetched data
```

---

## 🎯 Button/Action Endpoints (Data Modification)

### Create/Update/Delete Operations:

#### Tournament Actions:
| Action | Endpoint | Method | Input | Output |
|--------|----------|--------|-------|--------|
| Create tournament | `/api/tournaments/` | POST | Tournament data | Created tournament |
| Update tournament | `/api/tournaments/{id}/` | PUT/PATCH | Updated fields | Updated tournament |
| Delete tournament | `/api/tournaments/{id}/` | DELETE | - | 204 No Content |
| Register team | `/api/teams/` | POST | Team data | Created team |
| Add team member | `/api/teams/{id}/members/` | POST | Member data | Created member |
| Leave team | `/api/team-members/{id}/` | DELETE | - | 204 No Content |

#### Task Actions:
| Action | Endpoint | Method | Input | Output |
|--------|----------|--------|-------|--------|
| Submit code | `/api/submissions/` | POST | `{task_id, code, language}` | Created submission |
| Update submission | `/api/submissions/{id}/` | PATCH | `{code, language}` | Updated submission |
| Lock submission | `/api/submissions/{id}/lock/` | POST | - | Submission object |
| Unlock submission | `/api/submissions/{id}/unlock/` | POST | - | Submission object |
| Delete submission | `/api/submissions/{id}/` | DELETE | - | 204 No Content |

#### User Profile Actions:
| Action | Endpoint | Method | Input | Output |
|--------|----------|--------|-------|--------|
| Update profile | `/api/users/profile/update/` | PATCH | `{phone, address, date_of_birth}` | Updated profile |
| Enable 2FA | `/api/auth/2fa/enable/` | POST | - | 2FA setup info |
| Verify 2FA | `/api/auth/2fa/verify/` | POST | `{code, secret}` | Confirmation |
| Disable 2FA | `/api/auth/2fa/disable/` | POST | - | Confirmation |
| Forgot password | `/api/auth/forgot-password/` | POST | `{email}` | Confirmation |
| Reset password | `/api/auth/reset-password/` | POST | `{token, new_password}` | Confirmation |

---

## 🔌 Frontend Integration Guide

### 1. Authentication Setup

**Location:** `frontend/src/shared/context/AuthContext.jsx`

```javascript
// On app startup:
1. Check localStorage for access_token
2. If token exists:
   - Verify it's not expired
   - Call GET /api/auth/me/ to fetch current user
   - Store user in AuthContext
3. If token is missing/expired:
   - Redirect to login page

// On login:
1. POST /api/auth/login/ with email & password
2. Store access_token, refresh_token in localStorage
3. Call /api/auth/me/ to get full user profile
4. Store user data in AuthContext
5. Redirect to dashboard

// On token expiration (401 error):
1. POST /api/auth/refresh/ with refresh_token
2. Get new access_token
3. Update localStorage
4. Retry original API call with new token
```

### 2. API Client Setup

**Location:** `frontend/src/shared/api/client.js`

```javascript
// Configure axios instance:
- Base URL: http://localhost:8000/api/
- Auto-include Authorization header
- Auto-refresh tokens on 401
- Error handling for network failures

// Example API calls:
import { client } from './client.js'

// Get tournaments
const tournaments = await client.get('/tournaments/')

// Create submission
const submission = await client.post('/submissions/', {
  task_id: 1,
  code: 'print("hello")',
  language: 'python'
})

// Update profile
const profile = await client.patch('/users/profile/update/', {
  phone: '+380123456789',
  address: '123 Main St'
})
```

### 3. Dashboard Page Integration

**Endpoints to call:**
```
GET /api/auth/me/                    → User profile
GET /api/tournaments/                → List tournaments
GET /api/teams/                      → User's teams
GET /api/submissions/                → User's submissions
GET /api/tasks/?tournament_id=X      → Tasks for tournament
```

**Data rendering:**
```javascript
const [tournaments, setTournaments] = useState([])
const [userTeams, setUserTeams] = useState([])
const [submissions, setSubmissions] = useState([])

useEffect(() => {
  async function fetchData() {
    const tourn = await client.get('/tournaments/')
    const teams = await client.get('/teams/')
    const subs = await client.get('/submissions/')
    
    setTournaments(tourn.data.results)
    setUserTeams(teams.data.results)
    setSubmissions(subs.data.results)
  }
  fetchData()
}, [])
```

### 4. Tournament List Page

**Endpoints:**
```
GET /api/tournaments/                           → All tournaments
GET /api/tournaments/{id}/                      → Tournament details
GET /api/tournaments/{id}/teams/                → Tournament teams
GET /api/tournaments/{id}/statistics/           → Tournament stats
POST /api/teams/                                → Register team
```

**Filter/Search query params:**
```
?page=1                          → Pagination
&status=active                   → Filter by status
&created_by=1                    → Filter by creator
&ordering=-created_at            → Sort (- for descending)
&search=query                    → Search tournaments
```

### 5. Task List Page

**Endpoints:**
```
GET /api/tasks/                                 → All tasks
GET /api/tasks/{id}/                           → Task details
GET /api/tasks/{id}/requirements/               → Test cases
GET /api/tasks/{id}/statistics/                 → Task stats
```

**Filter query params:**
```
?tournament_id=X                 → Filter by tournament
&status=active                   → Filter by status
&difficulty=hard                 → Filter by difficulty
&search=keyword                  → Search tasks
&page=1&page_size=20            → Pagination
```

### 6. Submission Page

**Endpoints:**
```
POST /api/submissions/                          → Create submission
GET /api/submissions/{id}/                      → Get submission
PATCH /api/submissions/{id}/                    → Update submission
POST /api/submissions/{id}/lock/                → Lock submission
POST /api/submissions/{id}/unlock/              → Unlock submission
GET /api/submissions/by_team/?team_id=X        → Get team submissions
```

**Create submission:**
```json
{
  "task_id": 1,
  "code": "def solve():\n    pass",
  "language": "python"
}
```

### 7. Profile Page

**Endpoints:**
```
GET /api/auth/me/                              → Current profile
PATCH /api/users/profile/update/               → Update profile
POST /api/auth/2fa/enable/                     → Start 2FA setup
POST /api/auth/2fa/verify/                     → Verify 2FA
POST /api/auth/2fa/disable/                    → Disable 2FA
POST /api/auth/forgot-password/                → Request password reset
```

### 8. URL Patterns/Conventions

| Path | Frontend Route | Purpose |
|------|----------------|---------|
| `/dashboard` | DashboardPage | Main dashboard |
| `/tournaments` | TournamentListPage | Browse tournaments |
| `/tournaments/{id}` | TournamentDetailPage | Tournament details |
| `/tournaments/{id}/register` | TeamRegistrationPage | Register team |
| `/tasks` | TaskListPage | Browse tasks |
| `/tasks/{id}` | TaskDetailPage | Task details |
| `/tasks/{id}/submit` | SubmissionFormPage | Submit code |
| `/submissions` | SubmissionsListPage | User submissions |
| `/profile` | ProfilePage | User profile |
| `/settings` | SettingsPage | Settings |
| `/leaderboard` | LeaderboardPage | Leaderboard (NOT IMPLEMENTED) |

---

## ⚠️ Implementation Status

### ✅ FULLY IMPLEMENTED
- User authentication (login, register, refresh tokens)
- User profile management
- 2FA (Two-Factor Authentication)
- Password reset flow
- All task endpoints (CRUD + actions)
- All submission endpoints (CRUD + actions)
- All tournament endpoints (CRUD + actions)
- All team endpoints (CRUD + actions)
- API Gateway routing and proxying

### ⚠️ PARTIALLY IMPLEMENTED
- Dashboard - endpoints exist but frontend not fully connected
- Pagination - exists but not tested
- Filtering - exists but not fully utilized in frontend

### ❌ NOT IMPLEMENTED
- Jury assignment endpoints
- Leaderboard endpoints
- Scoring/ranking system
- Notifications system
- Real-time updates
- File uploads (for code submissions)
- Code execution/evaluation service
- Contest/round management

---

## 📝 Quick Reference: Common API Calls

### Authentication:
```bash
# Register
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","username":"user","password":"pass123","password_confirm":"pass123"}'

# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"pass123"}'

# Refresh token
curl -X POST http://localhost:8000/api/auth/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh":"<refresh_token>"}'

# Get current user
curl -X GET http://localhost:8000/api/auth/me/ \
  -H "Authorization: Bearer <access_token>"
```

### Tournament Management:
```bash
# List tournaments
curl -X GET "http://localhost:8000/api/tournaments/?status=active" \
  -H "Authorization: Bearer <access_token>"

# Get tournament details
curl -X GET http://localhost:8000/api/tournaments/1/ \
  -H "Authorization: Bearer <access_token>"

# Register team
curl -X POST http://localhost:8000/api/teams/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"tournament":1,"name":"Team Name","captain_name":"John","captain_email":"john@example.com","city":"Kyiv","contact":"+380123456789"}'
```

### Tasks & Submissions:
```bash
# List tasks
curl -X GET "http://localhost:8000/api/tasks/?tournament_id=1" \
  -H "Authorization: Bearer <access_token>"

# Submit code
curl -X POST http://localhost:8000/api/submissions/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"task_id":1,"code":"print(\"hello\")","language":"python"}'

# Get submissions
curl -X GET "http://localhost:8000/api/submissions/?team_id=1" \
  -H "Authorization: Bearer <access_token>"
```

---

## 🔗 Service Communication Summary

```
Frontend (Port 3000)
    ↓
API Gateway (Port 8000)
    ├→ User Service (Port 8001)
    │   ├ /api/auth/*
    │   ├ /api/users/*
    │   └ /api/teams/* (forwarded)
    │
    ├→ Task Service (Port 8002)
    │   ├ /api/tasks/*
    │   ├ /api/submissions/*
    │   └ /api/leaderboard/* (NOT IMPLEMENTED)
    │
    └→ Tournament Service (Port 8003)
        └ /api/tournaments/*
```

---

**Document Version:** 1.0  
**Last Updated:** May 15, 2026  
**Status:** Ready for Frontend Integration
