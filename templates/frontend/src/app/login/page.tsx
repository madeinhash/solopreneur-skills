'use client';

import React, { useEffect } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { useRouter } from 'next/navigation';
import { Button, Spin } from 'antd';
import { LoadingOutlined } from '@ant-design/icons';

export default function LoginPage() {
  const { isAuthenticated, loading, loginWithGoogle } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading && isAuthenticated) {
      router.push('/dashboard');
    }
  }, [isAuthenticated, loading, router]);

  const handleGoogleSignIn = () => {
    loginWithGoogle();
  };

  if (loading || isAuthenticated) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Spin indicator={<LoadingOutlined style={{ fontSize: 48 }} spin />} />
      </div>
    );
  }

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100">
      <div className="bg-white rounded-2xl shadow-lg p-8 w-full max-w-md mx-4">
        <div className="text-2xl font-bold text-center text-gray-900 mb-4">
          Welcome
        </div>

        <p className="text-center text-gray-600 text-sm mb-8">
          Sign in to continue
        </p>

        <Button
          onClick={handleGoogleSignIn}
          size="large"
          block
          className="h-12 rounded-lg font-medium"
        >
          Sign in with Google
        </Button>
      </div>
    </div>
  );
}
