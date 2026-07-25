import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { Spin } from 'antd';
import { useAuthContext } from '@/context/AuthContext';

/**
 * Route guard component that checks authentication state.
 * - Shows a loading spinner while auth state is being initialized.
 * - Redirects to /login if user is not authenticated.
 * - Renders the child route (Outlet) if authenticated.
 */
const ProtectedRoute: React.FC = () => {
  const { isAuthenticated, isLoading } = useAuthContext();

  if (isLoading) {
    return (
      <div
        style={{
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          height: '100vh',
        }}
      >
        <Spin size="large" tip="加载中..." />
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return <Outlet />;
};

export default ProtectedRoute;
