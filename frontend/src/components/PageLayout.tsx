import React, { useMemo } from 'react';
import { Outlet, useNavigate, useLocation } from 'react-router-dom';
import { Layout, Menu, Button, Dropdown, Typography, Breadcrumb } from 'antd';
import {
  DashboardOutlined,
  BugOutlined,
  PlayCircleOutlined,
  DesktopOutlined,
  UserOutlined,
  LogoutOutlined,
  HomeOutlined,
} from '@ant-design/icons';
import { useAuth } from '@/hooks/useAuth';

const { Header, Sider, Content } = Layout;
const { Text } = Typography;

// ---------------------------------------------------------------------------
// Navigation items
// ---------------------------------------------------------------------------

interface NavItem {
  key: string;
  label: string;
  icon: React.ReactNode;
  path: string;
}

const navItems: NavItem[] = [
  { key: 'dashboard', label: '仪表盘', icon: <DashboardOutlined />, path: '/dashboard' },
  { key: 'cases', label: '用例管理', icon: <BugOutlined />, path: '/cases' },
  { key: 'runs', label: '执行面板', icon: <PlayCircleOutlined />, path: '/runs' },
  { key: 'devices', label: '设备管理', icon: <DesktopOutlined />, path: '/devices' },
];

// ---------------------------------------------------------------------------
// Breadcrumb helpers
// ---------------------------------------------------------------------------

/** Path-to-label mapping for breadcrumb items. */
const breadcrumbLabelMap: Record<string, string> = {
  dashboard: '仪表盘',
  cases: '用例管理',
  runs: '执行面板',
  devices: '设备管理',
};

function buildBreadcrumbItems(pathname: string) {
  const segments = pathname.split('/').filter(Boolean);
  const items: { title: React.ReactNode }[] = [
    { title: <><HomeOutlined /> 首页</> },
  ];

  for (const segment of segments) {
    const label = breadcrumbLabelMap[segment] || segment;
    items.push({ title: label });
  }

  return items;
}

// ---------------------------------------------------------------------------
// PageLayout
// ---------------------------------------------------------------------------

/**
 * Main application layout with sidebar navigation, header bar, and content area.
 * Wraps child routes via React Router Outlet.
 */
const PageLayout: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { user, logout } = useAuth();

  // Determine selected menu key from current path
  const selectedKey = navItems.find((item) => location.pathname.startsWith(item.path))?.key || 'dashboard';

  const breadcrumbItems = useMemo(() => buildBreadcrumbItems(location.pathname), [location.pathname]);

  const handleMenuClick = (info: { key: string }) => {
    const item = navItems.find((n) => n.key === info.key);
    if (item) {
      navigate(item.path);
    }
  };

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  const userMenuItems = [
    {
      key: 'user-info',
      label: user?.username || '用户',
      disabled: true,
    },
    { type: 'divider' as const },
    {
      key: 'logout',
      label: '退出登录',
      icon: <LogoutOutlined />,
      onClick: handleLogout,
    },
  ];

  return (
    <Layout className="full-page">
      {/* Sidebar */}
      <Sider width={220} theme="dark" collapsible>
        <div style={{ height: 64, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          <Text strong style={{ color: '#fff', fontSize: 16 }}>
            EcoFlow 测试平台
          </Text>
        </div>
        <Menu
          theme="dark"
          mode="inline"
          selectedKeys={[selectedKey]}
          items={navItems.map((item) => ({
            key: item.key,
            icon: item.icon,
            label: item.label,
          }))}
          onClick={handleMenuClick}
        />
      </Sider>

      {/* Main area */}
      <Layout>
        {/* Header */}
        <Header
          style={{
            background: '#fff',
            padding: '0 24px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            borderBottom: '1px solid #f0f0f0',
            gap: 16,
          }}
        >
          <Breadcrumb items={breadcrumbItems} />
          <Dropdown menu={{ items: userMenuItems }} placement="bottomRight">
            <Button type="text" icon={<UserOutlined />}>
              {user?.username || '未登录'}
            </Button>
          </Dropdown>
        </Header>

        {/* Content */}
        <Content style={{ margin: 24, minHeight: 280 }}>
          <Outlet />
        </Content>
      </Layout>
    </Layout>
  );
};

export default PageLayout;
