# Backend — Express + TypeScript + Sequelize + PostgreSQL

## Quick Start

```bash
npm install
cp .env.template .env   # fill in DB credentials and JWT_SECRET
npm run db:migrate       # run database migrations
npm run dev              # start dev server with hot reload (tsx watch)
```

## Tech Stack

- **Runtime**: Node.js 22+
- **Language**: TypeScript (strict mode)
- **Framework**: Express 4
- **Database**: PostgreSQL with Sequelize 6 ORM
- **Auth**: JWT (jsonwebtoken)
- **Logging**: Pino with pino-pretty
- **Production**: PM2 process manager

## Project Structure

```
src/
├── index.ts                   # Express app entry point
├── router/                    # Route definitions
│   └── index.ts               # Router aggregator
├── controller/                # Request handlers (input validation, call services)
├── service/                   # Business logic
├── model/                     # Sequelize model definitions (schema for TS types & ORM)
├── db/
│   ├── sequelizeConfig.ts     # Sequelize instance & connection
│   ├── sequelizeConfigCommon.cjs  # Config for sequelize-cli (CommonJS)
│   ├── migrations/            # Database migration files (.cjs)
│   └── seeders/               # Seed data files
├── middleware/                # Express middleware (JWT auth, etc.)
└── utility/                   # Helpers (logger, response formatter, JWT, errors)
```

## Architecture: Router → Controller → Service → Model

- **Router**: Define HTTP routes and attach middleware
- **Controller**: Parse request, validate input, call service, return response
- **Service**: Business logic, database queries via models
- **Model**: Sequelize model definitions — used for type-checking and ORM queries only

## Scripts

| Command | Description |
|---------|-------------|
| `npm run dev` | Dev server with hot reload (tsx watch) |
| `npm run local` | Same as dev |
| `npm run build` | TypeScript compile to `dist/` |
| `npm run prod` | Clean → build → PM2 production |
| `npm run typecheck` | Type-check without emitting |
| `npm run db:migrate` | Run pending migrations |
| `npm run db:migrate:undo` | Rollback last migration |
| `npm run db:migration:create` | Create new migration file |

## Database Migrations (IMPORTANT)

**Always use migrations for schema changes. Never use `sequelize.sync()`.**

- Migration files go in `src/db/migrations/` as `.cjs` files (CommonJS for sequelize-cli)
- Naming convention: `YYYYMMDDHHMMSS-description.cjs`
- Create a new migration: `npm run db:migration:create -- --name add-column-to-users`
- Run migrations: `npm run db:migrate`
- Rollback: `npm run db:migrate:undo`
- Migration tracking table: `sequelize_migration_record`

### Adding a new table

1. Create the migration file in `src/db/migrations/`
2. Create the model file in `src/model/` (for TypeScript types and Sequelize ORM)
3. The model must match the migration schema exactly

## Coding Conventions

- All source code in TypeScript (`.ts`), migrations in CommonJS (`.cjs`)
- Use `import`/`export` (ESM) — project has `"type": "module"` in package.json
- Import paths must include `.js` extension (NodeNext module resolution)
- Use `(req as any).user` for accessing JWT-decoded user data on request objects
- Error classes extend `BaseError` in `utility/error/`
- Use `response()` helper for all HTTP responses
- Structured logging via `logger` (pino) — never use `console.log` in production code

## Environment Variables

See `.env.template` for all required variables. Key ones:
- `PORT` — server port (default 4000)
- `NODE_ENV` — development | production
- `DB_*` — PostgreSQL connection details
- `JWT_SECRET` — JWT signing secret
- `CORS_WHITELIST` — comma-separated allowed origins
