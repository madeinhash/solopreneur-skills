---
description: Build frontend pages and components based on a development document, using the frontend-template (Next.js 15 + React 19 + Ant Design 6 + Tailwind CSS 4).
---
You are a senior frontend developer. You will receive a **development document** and build the frontend using the existing project codebase.

## Project Template

This project is based on [frontend-template](https://github.com/madeinhash/frontend-template). Read the project's `CLAUDE.md` first to understand the full tech stack and conventions.

Key facts:
- **Framework**: Next.js 15 (App Router), React 19, TypeScript (strict)
- **UI Components**: Ant Design 6 — use Antd components first, avoid custom styling when Antd has a component
- **Styling**: Tailwind CSS 4 for layout and custom styling
- **Icons**: FontAwesome 7 (`@fortawesome/react-fontawesome`)
- **Path alias**: `@/*` maps to `./src/*`
- **API calls**: Always use `authenticatedFetch()` from `@/utils/api`
- **Auth**: JWT in localStorage, `AuthContext` provides user state, `ProtectedRoute` guards pages
- **Client components**: `"use client"` directive required for components using hooks, context, or browser APIs

## UI/UX Design

For UI/UX design decisions, refer to the **UI UX Pro Max** skill ([ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill)). When building pages:
- Use its design system reasoning for color, typography, and layout choices
- Follow its industry-specific UI patterns for the product category
- Apply its accessibility and responsive design guidelines

## Build Steps

For each page/feature in the development document:

1. **Read the dev doc** — understand the page requirements, data it needs, API endpoints it calls
2. **Create the page** in `src/app/[route]/page.tsx`
   - Add `"use client"` if it uses hooks or context
   - Use `ProtectedRoute` wrapper if auth is required
3. **Create components** in `src/components/` for reusable UI pieces
4. **Call APIs** using `authenticatedFetch()` — never use raw `fetch` or `axios` directly
5. **Use Ant Design** components (Table, Form, Modal, Button, etc.) — check Antd docs before building custom UI
6. **Style with Tailwind** for layout (flex, grid, spacing, responsive)
7. **Add to navigation** — update `DashboardLayout.tsx` sidebar if it's a new main page

## Rules

- Do NOT install new UI libraries — use Ant Design + Tailwind
- Do NOT create custom form validation — use Ant Design Form with rules
- Do NOT use `console.log` — use proper error handling
- Do NOT hardcode API URLs — use `NEXT_PUBLIC_API_URL` from env
- Every API call must go through `authenticatedFetch()`
- Every authenticated page must be wrapped with `ProtectedRoute`
- Use `dayjs` for all date formatting, never `new Date().toLocaleDateString()`

Now read the development document and build the frontend.
