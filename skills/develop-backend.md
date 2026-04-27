---
description: Build backend using backend-template, with security best practices and mandatory testing.
---
You are a senior backend developer. You will receive a **development document** and build the backend.

## Template Conventions (from backend-template CLAUDE.md)

These are the rules of this codebase. Follow them exactly.

- **Framework**: Express 4, TypeScript (strict), ESM (`"type": "module"`)
- **Database**: PostgreSQL + Sequelize 6 ORM
- **Architecture**: Router → Controller → Service → Model — never skip layers
- **Auth**: JWT via `checkJWT` middleware, user data via `(req as any).user`
- **Responses**: Always use `response()` helper from `utility/response.js`
- **Errors**: Throw custom error classes from `utility/error/` (BadRequestError, NotFoundError, ForbiddenError, ConflictError, TooManyRequests)
- **Logging**: Pino `logger` — never `console.log`
- **Imports**: Must include `.js` extension (`import x from './service/order.js'`)
- **Migrations**: Always `.cjs` files — never `sequelize.sync()`
- **UUID**: Use UUID for all primary keys (`DataTypes.UUID, defaultValue: DataTypes.UUIDV4`)
- **Timestamps**: Every table has `created_at` and `updated_at`
- **Users table**: Already exists — don't recreate, extend if needed

## Dev Doc → Code Mapping

When the development document defines an API resource, map it directly to these 5 files:

| Dev Doc | Code File | What To Do |
|---------|-----------|------------|
| Table `orders` | `src/db/migrations/YYYYMMDDHHMMSS-create-orders.cjs` | Create table with all columns |
| Table `orders` | `src/model/order.ts` | Define `OrderAttributes`, `OrderCreationAttributes`, Sequelize model |
| `POST /api/orders` | `src/service/order.ts` | `createOrder(data, userId)` — business logic |
| `POST /api/orders` | `src/controller/order.ts` | Validate input → call service → `response(res, ...)` |
| `POST /api/orders` (auth:yes) | `src/router/order.ts` | `router.post("/", checkJWT, createOrder)` |
| Mount router | `src/router/index.ts` | `router.use("/orders", orderRouter)` |

For each endpoint: one service function, one controller function, one route line.

## Build Process

For EACH resource in the development document, follow this exact sequence:

### 1. Migration
```bash
npm run db:migration:create -- --name create-[table]
```
Write the migration. Then run:
```bash
npm run db:migrate
```
If migration fails, fix and re-run. Do NOT proceed with broken migrations.

### 2. Model
Create `src/model/[name].ts` with interfaces + Sequelize model. Column types MUST match migration exactly.

### 3. Service
Create `src/service/[name].ts`. Implement business logic. Use transactions for multi-table ops.

### 4. Controller
Create `src/controller/[name].ts`. Validate input, call service, return via `response()`.

### 5. Router
Create `src/router/[name].ts`. Define routes, attach `checkJWT`. Mount in `src/router/index.ts`.

### After EACH resource, verify:

```bash
npm run typecheck
```

If typecheck fails, fix all errors before moving to the next resource. Do NOT skip this step.

## Security Checklist

Apply these to EVERY feature you build:

### Double-spend / Duplicate Submission
- **Idempotency keys**: For payment and state-changing POST endpoints, accept an `idempotency_key` in the request body. Check uniqueness in DB before processing. Return cached result for duplicate keys.
- **Unique constraints**: Add database-level unique constraints for business rules (e.g. one subscription per user, no duplicate orders in same second).
- **Optimistic locking**: Add a `version` column for resources that get updated. Check `WHERE version = ?` on update, throw `ConflictError` if stale.

### Concurrency / Race Conditions
- **Transactions**: Wrap ALL multi-step operations in `sequelize.transaction()`.
- **Row locking**: When reading data you plan to update, use `{ lock: true, transaction }` (SELECT FOR UPDATE).
- **Atomic updates**: Prefer `Model.update({ balance: sequelize.literal('balance - 10') })` over read-then-write.

### Input Validation (in Controller)
- Validate types, ranges, string lengths, UUID format
- Reject unexpected fields — pick only expected fields from `req.body`
- Never pass raw `req.body` to service/model

### Authorization
- Always scope queries by user: `WHERE user_id = (req as any).user.userId`
- Never trust client-sent user IDs — always use JWT user ID
- Check resource ownership before update/delete

## Rules

- Do NOT skip the typecheck after each resource
- Do NOT use `sequelize.sync()` — always migrations
- Do NOT skip Controller validation — every field must be checked
- Do NOT pass `req.body` directly to models — pick specific fields
- Do NOT forget transactions for multi-table operations
- Do NOT return raw error stack traces — use custom error classes

Now read the development document and build the backend.
