# Development Document — [Project Name]

## 1. Overview

**Project Name**:
**One-line Description**:
**Target Users**:

## 2. Core Features

List each feature with a brief description:

1. **Feature Name** — description
2. **Feature Name** — description
3. **Feature Name** — description

## 3. Tech Stack

| Layer | Technology | Template |
|-------|-----------|----------|
| Frontend | Next.js 15 + React 19 + TypeScript + Ant Design 6 + Tailwind CSS 4 | [frontend-template](https://github.com/madeinhash/frontend-template) |
| Backend | Express + TypeScript + Sequelize + PostgreSQL | [backend-template](https://github.com/madeinhash/backend-template) |
| Agent (if needed) | Python + LiteLLM + Claude Code Architecture | [agent-template](https://github.com/madeinhash/agent-template) |

## 4. Data Model

Define all database tables. Each table needs:
- Table name
- All columns with types
- Relationships (foreign keys)

### Table: `users`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PK, default uuid | |
| email | VARCHAR(255) | UNIQUE, NOT NULL | |
| name | VARCHAR(255) | | |
| avatar_url | TEXT | | |
| created_at | TIMESTAMP | NOT NULL | |
| updated_at | TIMESTAMP | NOT NULL | |

### Table: `[table_name]`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| | | | |

## 5. API Endpoints

Define all API endpoints. Group by resource.

### Auth

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | /api/auth/google | No | Redirect to Google OAuth |
| GET | /api/auth/google/callback | No | OAuth callback, returns JWT |

### [Resource Name]

| Method | Path | Auth | Description | Request Body | Response |
|--------|------|------|-------------|-------------|----------|
| GET | /api/[resource] | Yes | List all | — | `{ data: [...] }` |
| POST | /api/[resource] | Yes | Create | `{ field1, field2 }` | `{ data: {...} }` |
| GET | /api/[resource]/:id | Yes | Get by ID | — | `{ data: {...} }` |
| PUT | /api/[resource]/:id | Yes | Update | `{ field1 }` | `{ data: {...} }` |
| DELETE | /api/[resource]/:id | Yes | Delete | — | `{ message: "deleted" }` |

## 6. Pages & Routes (Frontend)

| Route | Page | Auth Required | Description |
|-------|------|---------------|-------------|
| `/` | Home | No | Landing / redirect to login |
| `/login` | Login | No | Google OAuth login |
| `/dashboard` | Dashboard | Yes | Main dashboard |
| `/[page]` | [Page] | Yes | [Description] |

## 7. Agent Tools (if applicable)

Only fill this if the project includes an AI agent.

| Tool Name | Description | Read-only |
|-----------|-------------|-----------|
| | | |

## 8. Implementation Order

Recommended build sequence:

1. **Database** — Create migrations for all tables
2. **Backend API** — Build endpoints (Router → Controller → Service → Model)
3. **Frontend pages** — Build UI pages consuming the API
4. **Agent** (if needed) — Add custom tools and skills
5. **Integration testing** — End-to-end flow verification
