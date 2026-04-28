# Frontend — Next.js 15 + React 19 + TypeScript

## Quick Start

```bash
npm install
cp .env.template .env.local   # set NEXT_PUBLIC_API_URL
npm run dev                    # start dev server on port 3000
```

## Tech Stack

- **Framework**: Next.js 15 (App Router, Turbopack)
- **UI Library**: React 19
- **Language**: TypeScript (strict mode)
- **UI Components**: Ant Design 6
- **Styling**: Tailwind CSS 4
- **Icons**: FontAwesome 7
- **HTTP Client**: Axios
- **Date**: dayjs

## Project Structure

```
src/
├── app/                       # Next.js App Router pages
│   ├── layout.tsx             # Root layout with providers
│   ├── page.tsx               # Home page (/)
│   ├── login/page.tsx         # Login page
│   └── dashboard/page.tsx     # Dashboard page
├── components/                # Reusable React components
│   ├── DashboardLayout.tsx    # Sidebar layout wrapper
│   ├── LayoutWrapper.tsx      # Conditional layout renderer
│   └── ProtectedRoute.tsx     # Auth route guard
├── contexts/                  # React Context providers
│   └── AuthContext.tsx         # Authentication state & methods
├── hooks/                     # Custom React hooks
├── lib/                       # Third-party library configs
│   ├── AntdRegistry.tsx       # Ant Design SSR setup
│   └── Fontawesome.tsx        # FontAwesome icon setup
├── utils/                     # Utility functions
│   └── api.ts                 # API fetch wrapper with 401 auto-logout
└── const/                     # Constants
    └── styles.ts              # Style constants
```

## Scripts

| Command | Description |
|---------|-------------|
| `npm run dev` | Dev server with Turbopack |
| `npm run build` | Production build |
| `npm run start` | Run production build |
| `npm run lint` | ESLint check |

## Authentication Flow

1. Google OAuth redirect via `loginWithGoogle()`
2. Backend returns JWT token via URL parameter
3. Frontend stores JWT in `localStorage` (key: `app:jwt`)
4. `AuthContext` provides `user`, `isAuthenticated`, `loading` state
5. `ProtectedRoute` guards authenticated pages
6. `authenticatedFetch()` auto-attaches Bearer token, auto-logout on 401

## Coding Conventions

- All pages use Next.js App Router (`src/app/`)
- Path alias: `@/*` maps to `./src/*`
- Use `authenticatedFetch()` from `utils/api.ts` for all API calls
- Ant Design components for UI — avoid custom styling when Antd has a component
- Tailwind for layout and custom styling
- Use `dayjs` for date formatting
- Use FontAwesome icons (`@fortawesome/react-fontawesome`) — avoid mixing with other icon libraries
- `"use client"` directive required for components using hooks, context, or browser APIs

## Environment Variables

- `NEXT_PUBLIC_API_URL` — Backend API base URL (default `http://localhost:4000`)
