# Frontend Template

Next.js 15 + React 19 + TypeScript + Ant Design + Tailwind CSS frontend template

## Directory Structure

```
src/
├── app/                  # Page routes (Next.js App Router)
│   ├── layout.tsx        # Root layout: Provider wrappers, global styles
│   ├── page.tsx          # Home page
│   ├── login/            # Login page
│   └── dashboard/        # Dashboard page
├── components/           # Component layer
│   ├── DashboardLayout.tsx   # Dashboard layout (with sidebar)
│   ├── LayoutWrapper.tsx     # Layout wrapper (determines if layout is needed)
│   └── ProtectedRoute.tsx    # Route guard (requires login)
├── contexts/             # Global state (React Context)
│   └── AuthContext.tsx   # Authentication state management
├── hooks/                # Custom Hooks
├── lib/                  # Third-party library configs
│   ├── AntdRegistry.tsx  # Ant Design SSR config
│   └── Fontawesome.tsx   # FontAwesome icon config
├── utils/                # Utility functions
│   └── api.ts            # API request wrapper
└── const/                # Constants
    └── styles.ts         # Style constants
```

## Layer Responsibilities

| Layer | Responsibility | Example |
|---|---|---|
| **app/** | Page routes, each folder is a route | `app/users/page.tsx` → `/users` |
| **components/** | Reusable UI components | Button, Modal, Table, etc. |
| **contexts/** | Global state management | User auth, theme, language, etc. |
| **hooks/** | Custom React Hooks | `useFetch`, `useDebounce` |
| **utils/** | Utility functions | API wrapper, formatters, validators |
| **lib/** | Third-party library configs | Ant Design, icon libraries |

## Page Routing Rules

```
src/app/
├── page.tsx              → /
├── login/page.tsx        → /login
├── dashboard/page.tsx    → /dashboard
├── users/
│   ├── page.tsx          → /users
│   └── [id]/page.tsx     → /users/:id (dynamic route)
└── settings/
    ├── layout.tsx        → Nested layout
    └── page.tsx          → /settings
```

## Getting Started

1. Copy environment variables file
```bash
cp .env.template .env
```

2. Configure API URL in `.env`

3. Install dependencies
```bash
npm install
```

4. Start development server
```bash
npm run dev
```

## Adding New Features Examples

### 1. Add New Page

Create file `src/app/users/page.tsx`:
```tsx
'use client';

import { useState, useEffect } from 'react';
import { Table } from 'antd';
import { useAuth } from '@/contexts/AuthContext';

export default function UsersPage() {
  const { getToken } = useAuth();
  const [users, setUsers] = useState([]);

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/users`, {
      headers: { Authorization: `Bearer ${getToken()}` }
    })
      .then(res => res.json())
      .then(data => setUsers(data));
  }, []);

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Users</h1>
      <Table dataSource={users} columns={[...]} />
    </div>
  );
}
```

### 2. Add New Component

Create file `src/components/UserCard.tsx`:
```tsx
interface UserCardProps {
  name: string;
  email: string;
  avatar?: string;
}

export default function UserCard({ name, email, avatar }: UserCardProps) {
  return (
    <div className="p-4 bg-white rounded-lg shadow">
      <img src={avatar} alt={name} className="w-12 h-12 rounded-full" />
      <h3 className="font-bold">{name}</h3>
      <p className="text-gray-500">{email}</p>
    </div>
  );
}
```

### 3. Add New Context

Create file `src/contexts/ThemeContext.tsx`:
```tsx
'use client';

import { createContext, useContext, useState, ReactNode } from 'react';

type Theme = 'light' | 'dark';

interface ThemeContextType {
  theme: Theme;
  toggleTheme: () => void;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export const useTheme = () => {
  const context = useContext(ThemeContext);
  if (!context) throw new Error('useTheme must be used within ThemeProvider');
  return context;
};

export const ThemeProvider = ({ children }: { children: ReactNode }) => {
  const [theme, setTheme] = useState<Theme>('light');

  const toggleTheme = () => {
    setTheme(prev => prev === 'light' ? 'dark' : 'light');
  };

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
};
```

Use in `app/layout.tsx`:
```tsx
import { ThemeProvider } from '@/contexts/ThemeContext';

export default function RootLayout({ children }) {
  return (
    <ThemeProvider>
      {children}
    </ThemeProvider>
  );
}
```

### 4. Add Custom Hook

Create file `src/hooks/useFetch.ts`:
```tsx
import { useState, useEffect } from 'react';
import { useAuth } from '@/contexts/AuthContext';

export function useFetch<T>(url: string) {
  const { getToken } = useAuth();
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    fetch(url, {
      headers: { Authorization: `Bearer ${getToken()}` }
    })
      .then(res => res.json())
      .then(setData)
      .catch(setError)
      .finally(() => setLoading(false));
  }, [url]);

  return { data, loading, error };
}
```

## Commands

```bash
npm run dev    # Development server (Turbo)
npm run build  # Build for production
npm run start  # Run production build
npm run lint   # Code linting
```

## Tech Stack

- **Next.js 15** - React framework
- **React 19** - UI library
- **TypeScript** - Type safety
- **Ant Design 6** - UI component library
- **Tailwind CSS 4** - Styling framework
- **FontAwesome** - Icon library
# frontend-template
