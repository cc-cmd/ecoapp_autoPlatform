import React from 'react';
import ReactDOM from 'react-dom/client';
import { QueryClient, QueryClientProvider, QueryCache } from '@tanstack/react-query';
import { ConfigProvider, message } from 'antd';
import zhCN from 'antd/locale/zh_CN';
import { AuthProvider } from '@/context/AuthContext';
import App from '@/App';
import '@/styles/global.css';

// ---------------------------------------------------------------------------
// React Query client
// ---------------------------------------------------------------------------

const queryClient = new QueryClient({
  queryCache: new QueryCache({
    onError: (error) => {
      // 401 is handled by axios interceptor (redirect to /login), don't double-notify
      const axiosError = error as { response?: { status?: number } };
      if (axiosError.response?.status === 401) return;
      message.error(error instanceof Error ? error.message : '请求失败');
    },
  }),
  defaultOptions: {
    queries: {
      staleTime: 30_000,    // 30s default stale time
      retry: 1,             // Retry once on failure
      refetchOnWindowFocus: false,
    },
    mutations: {
      retry: 0,
    },
  },
});

// ---------------------------------------------------------------------------
// Render
// ---------------------------------------------------------------------------

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <ConfigProvider locale={zhCN} theme={{ token: { colorPrimary: '#1677ff' } }}>
          <App />
        </ConfigProvider>
      </AuthProvider>
    </QueryClientProvider>
  </React.StrictMode>,
);
