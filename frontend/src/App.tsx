import React, { lazy, Suspense } from 'react';
import { createBrowserRouter, RouterProvider, Navigate } from 'react-router-dom';
import { Spin } from 'antd';
import { PageLayout, ProtectedRoute, ErrorBoundary } from '@/components';

// ---------------------------------------------------------------------------
// Lazy-loaded pages
// ---------------------------------------------------------------------------

const LoginPage = lazy(() => import('@/pages/Login'));
const RegisterPage = lazy(() => import('@/pages/Register'));
const DashboardPage = lazy(() => import('@/pages/Dashboard'));
const CasesPage = lazy(() => import('@/pages/Cases'));
const CaseDetailPage = lazy(() => import('@/pages/CaseDetail'));
const RunsPage = lazy(() => import('@/pages/Runs'));
const RunDetailPage = lazy(() => import('@/pages/RunDetail'));
const DevicesPage = lazy(() => import('@/pages/Devices'));

// ---------------------------------------------------------------------------
// Suspense fallback
// ---------------------------------------------------------------------------

const PageLoading: React.FC = () => (
  <div
    style={{
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      minHeight: 400,
    }}
  >
    <Spin size="large" tip="页面加载中..." />
  </div>
);

const SuspenseWrapper: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <Suspense fallback={<PageLoading />}>{children}</Suspense>
);

// ---------------------------------------------------------------------------
// NotFound page
// ---------------------------------------------------------------------------

const NotFoundPage: React.FC = () => (
  <div
    style={{
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      minHeight: '100vh',
      flexDirection: 'column',
    }}
  >
    <h1>404</h1>
    <p>页面不存在</p>
    <a href="/">返回首页</a>
  </div>
);

// ---------------------------------------------------------------------------
// Router
// ---------------------------------------------------------------------------

const router = createBrowserRouter([
  {
    path: '/login',
    element: (
      <SuspenseWrapper>
        <LoginPage />
      </SuspenseWrapper>
    ),
  },
  {
    path: '/register',
    element: (
      <SuspenseWrapper>
        <RegisterPage />
      </SuspenseWrapper>
    ),
  },
  {
    path: '/',
    element: <ProtectedRoute />,
    children: [
      {
        element: <PageLayout />,
        children: [
          {
            index: true,
            element: <Navigate to="/dashboard" replace />,
          },
          {
            path: 'dashboard',
            element: (
              <SuspenseWrapper>
                <DashboardPage />
              </SuspenseWrapper>
            ),
          },
          {
            path: 'cases',
            element: (
              <SuspenseWrapper>
                <CasesPage />
              </SuspenseWrapper>
            ),
          },
          {
            path: 'cases/:id',
            element: (
              <SuspenseWrapper>
                <CaseDetailPage />
              </SuspenseWrapper>
            ),
          },
          {
            path: 'runs',
            element: (
              <SuspenseWrapper>
                <RunsPage />
              </SuspenseWrapper>
            ),
          },
          {
            path: 'runs/:id',
            element: (
              <SuspenseWrapper>
                <RunDetailPage />
              </SuspenseWrapper>
            ),
          },
          {
            path: 'devices',
            element: (
              <SuspenseWrapper>
                <DevicesPage />
              </SuspenseWrapper>
            ),
          },
        ],
      },
    ],
  },
  {
    path: '*',
    element: <NotFoundPage />,
  },
]);

// ---------------------------------------------------------------------------
// App
// ---------------------------------------------------------------------------

/**
 * Root application component wrapped in ErrorBoundary.
 */
const App: React.FC = () => {
  return (
    <ErrorBoundary>
      <RouterProvider router={router} />
    </ErrorBoundary>
  );
};

export default App;
