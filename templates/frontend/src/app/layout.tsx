// app/layout.tsx
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import { AuthProvider } from '@/contexts/AuthContext';
import '@/lib/Fontawesome';
import AntdRegistry from '@/lib/AntdRegistry';
import LayoutWrapper from '@/components/LayoutWrapper';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'App Template',
  description: 'A Next.js template with authentication',
  icons: {
    icon: '/favicon.ico',
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className} suppressHydrationWarning>
        <AuthProvider>
          <AntdRegistry>
            <LayoutWrapper>{children}</LayoutWrapper>
          </AntdRegistry>
        </AuthProvider>
      </body>
    </html>
  );
}
