# Development Document — [Project Name]

## 1. Overview

**Project Name**:
**One-line Description**:
**Target Users**:

## 2. Core Features

1. **Feature Name** — description
2. **Feature Name** — description
3. **Feature Name** — description

## 3. Tech Stack

| Layer | Technology | Template Repo |
|-------|-----------|---------------|
| Frontend | Next.js 15 + React 19 + TypeScript + Ant Design 6 + Tailwind CSS 4 | [frontend-template](https://github.com/madeinhash/frontend-template) |
| Backend | Express + TypeScript + Sequelize + PostgreSQL | [backend-template](https://github.com/madeinhash/backend-template) |
| Agent (if needed) | Python + LiteLLM + Claude Code Architecture (port 8080) | [agent-template](https://github.com/madeinhash/agent-template) |

## 4. Data Model

Define every table. The `users` table already exists in the template — only list new tables or extensions.

Format for each table:

### Table: `[table_name]`

```
Column          | Type           | Constraints              | Description
----------------|----------------|--------------------------|------------
id              | UUID           | PK, default UUIDV4       |
user_id         | UUID           | FK → users.id, NOT NULL  |
name            | VARCHAR(255)   | NOT NULL                 |
status          | ENUM           | 'active','inactive'      |
amount          | DECIMAL(10,2)  | NOT NULL, default 0      |
created_at      | TIMESTAMP      | NOT NULL                 |
updated_at      | TIMESTAMP      | NOT NULL                 |
```

Indexes: `[list any unique constraints or indexes]`

## 5. API Endpoints

Format for each endpoint — this maps directly to backend code:

### Resource: `[resource_name]`

```
METHOD  PATH                AUTH    DESCRIPTION
------  ----                ----    -----------
GET     /api/orders         yes     List user's orders
POST    /api/orders         yes     Create order
GET     /api/orders/:id     yes     Get order by ID
PUT     /api/orders/:id     yes     Update order
DELETE  /api/orders/:id     yes     Delete order
```

For each POST/PUT, define the request body:

**POST /api/orders**
```json
{
  "product_id": "UUID (required)",
  "quantity": "integer (required, min: 1)",
  "note": "string (optional, max: 500)"
}
```

**Response format** (all endpoints):
```json
{
  "statusCode": 200,
  "message": "Success",
  "data": { ... }
}
```

Security notes for this resource:
- [ ] Needs idempotency key (payment/state-change)
- [ ] Needs row locking (concurrent updates)
- [ ] Needs rate limiting
- [ ] Needs ownership check (user can only access own data)

## 6. Pages & Routes (Frontend)

Format for each page — this maps directly to frontend code:

```
ROUTE                   AUTH    PAGE COMPONENT              DESCRIPTION
-----                   ----    --------------              -----------
/                       no      Home                        Landing / redirect to login
/login                  no      Login                       Google OAuth login (exists in template)
/dashboard              yes     Dashboard                   Main dashboard (exists in template)
/dashboard/orders       yes     OrderList                   Table of user's orders
/dashboard/orders/:id   yes     OrderDetail                 Single order detail view
/dashboard/orders/new   yes     OrderCreate                 Create order form
```

For each page, list the API calls it makes:
- **OrderList**: `GET /api/orders` → display in Ant Design `<Table>`
- **OrderCreate**: `POST /api/orders` → Ant Design `<Form>` + `<Modal>`

## 7. Agent Tools (if applicable)

Only if the project includes an AI agent (port 8080).

```
TOOL NAME       READ-ONLY   DESCRIPTION
---------       ---------   -----------
search_db       yes         Search the database for relevant records
send_email      no          Send an email notification to user
```

## 8. Implementation Order

1. **Database** — Create all migrations, run `npm run db:migrate`
2. **Backend API** — Build each resource: Migration → Model → Service → Controller → Router → `npm run typecheck`
3. **Frontend** — Build each page with UI UX Pro Max skill for design → `npm run build`
4. **Agent** (if needed) — Build each tool → register → `pytest`
5. **Integration** — Test full flow end-to-end
