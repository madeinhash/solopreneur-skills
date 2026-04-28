// src/components/LayoutWrapper.tsx
'use client';

import { usePathname } from 'next/navigation';
import DashboardLayout from '@/components/DashboardLayout';

export default function LayoutWrapper({
  children,
}: {
  children: React.ReactNode;
}) {
  const pathname = usePathname();

  // Public pages (no auth required)
  const publicRoutes = ['/', '/login'];

  const needsLayout = !publicRoutes.includes(pathname || '');

  if (!needsLayout) {
    return <>{children}</>;
  }

  return <DashboardLayout>{children}</DashboardLayout>;
}
