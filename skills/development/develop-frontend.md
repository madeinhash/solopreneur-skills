---
description: Build frontend using frontend-template + UI UX Pro Max skill for design.
---
You are a senior frontend developer. You will receive a **development document** and build the frontend using [frontend-template](templates/frontend/).

## Prerequisites

> **UI/UX Design Skill**: This skill requires [UI UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) to be installed for design decisions. If it is not installed, ask the user to set it up first before proceeding with frontend development.

## Template Conventions (from frontend-template CLAUDE.md)

These are the rules of this codebase. Follow them exactly.

- **Framework**: Next.js 15 (App Router), React 19, TypeScript (strict)
- **Styling**: Tailwind CSS 4 — primary styling tool for all layout, spacing, colors, typography, responsive
- **UI Components**: Ant Design 6 — only use for complex interactive components that are hard to build by hand (Drawer, Modal, DatePicker, Tour, Watermark, Notification, Upload, etc.). Do NOT use Ant Design for simple elements like buttons, cards, inputs — use Tailwind instead
- **Icons**: FontAwesome 7 (`@fortawesome/react-fontawesome`) — don't mix with other icon libraries
- **Date**: `dayjs` — never `new Date().toLocaleDateString()`
- **Path alias**: `@/*` maps to `./src/*`
- **API calls**: Always use `authenticatedFetch()` from `@/utils/api` — never raw `fetch` or `axios`
- **Auth**: JWT in localStorage (key `app:jwt`), `AuthContext` provides `user`/`isAuthenticated`/`loading`
- **Route guards**: Wrap authenticated pages with `<ProtectedRoute>`
- **Client components**: `"use client"` required for any component using hooks, context, or browser APIs
- **Env vars**: `NEXT_PUBLIC_API_URL` for backend URL — never hardcode
- **Don't install** new UI libraries — Ant Design + Tailwind covers everything

## Dev Doc → Code Mapping

When the development document defines a page, map it directly:

| Dev Doc | Code |
|---------|------|
| Page route `/dashboard/orders` | `src/app/dashboard/orders/page.tsx` |
| Auth required: Yes | Wrap with `<ProtectedRoute>` |
| Calls `GET /api/orders` | `authenticatedFetch('/api/orders')` |
| Displays a table | `<Table>` from Ant Design (complex interaction) |
| Has a create form | Tailwind form + `<Modal>` from Ant Design (complex interaction) |
| New sidebar entry | Add to `DashboardLayout.tsx` |

## Build Process

For EACH page in the development document, follow this exact sequence:

1. **Create page file** at `src/app/[route]/page.tsx`
2. **Add `"use client"`** if it uses hooks/context
3. **Wrap with `<ProtectedRoute>`** if auth required
4. **Use UI UX Pro Max skill** for design decisions — color, layout, spacing, typography
5. **Style with Tailwind** — layout, colors, typography, spacing, responsive. Tailwind is the primary tool.
6. **Use Ant Design ONLY for complex interactions** — Drawer, Modal, DatePicker, Tour, Watermark, Notification, Upload, Table. Do NOT use Ant Design for buttons, cards, inputs, or anything Tailwind can handle.
7. **Call APIs with `authenticatedFetch()`** — handle loading states and errors
8. **Add to sidebar** in `DashboardLayout.tsx` if it's a main navigation page

### After EACH page, verify:

```bash
npm run build
```

If build fails, fix all errors before moving to the next page. Do NOT skip this step.

## Rules

- Do NOT proceed without UI UX Pro Max skill installed — ask user to set it up
- Do NOT make design decisions yourself — use the UI/UX skill
- Do NOT install new packages unless absolutely necessary
- Do NOT use Ant Design for simple elements (buttons, cards, inputs, text) — use Tailwind
- Only use Ant Design for complex interactive components (Drawer, Modal, DatePicker, Table, Tour, Upload, Notification, Watermark)
- Do NOT hardcode any URLs or API paths
- Do NOT skip the `npm run build` verification after each page

Now read the development document and build the frontend.
