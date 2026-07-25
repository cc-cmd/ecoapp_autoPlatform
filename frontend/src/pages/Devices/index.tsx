import React from 'react';
import { Card, Table, Button, Typography, Space, message, Alert } from 'antd';
import { ReloadOutlined } from '@ant-design/icons';
import dayjs from 'dayjs';
import relativeTime from 'dayjs/plugin/relativeTime';
import StatusTag from '@/components/StatusTag';
import { useDevices, useDiscoverDevices } from '@/hooks/useDevices';
import type { Device, Platform } from '@/types';

// Extend dayjs with relative time plugin
dayjs.extend(relativeTime);

const { Title, Text } = Typography;

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

/**
 * Format last_heartbeat as relative time.
 * - <10s: "刚刚"
 * - <60s: "N秒前"
 * - <5min: "N分钟前"
 * - else: absolute
 */
function formatRelativeTime(dateStr: string | undefined): string {
  if (!dateStr) return '-';
  const now = dayjs();
  const date = dayjs(dateStr);
  const diffSeconds = now.diff(date, 'second');

  if (diffSeconds < 10) return '刚刚';
  if (diffSeconds < 60) return `${diffSeconds}秒前`;
  if (diffSeconds < 300) return `${now.diff(date, 'minute')}分钟前`;

  return date.format('YYYY-MM-DD HH:mm:ss');
}

// ---------------------------------------------------------------------------
// Columns
// ---------------------------------------------------------------------------

const columns = [
  {
    title: '设备名称',
    dataIndex: 'name',
    key: 'name',
  },
  {
    title: 'UDID',
    dataIndex: 'udid',
    key: 'udid',
    ellipsis: true,
    width: 200,
  },
  {
    title: '平台',
    dataIndex: 'platform',
    key: 'platform',
    width: 100,
    render: (platform: Platform) => (
      <Text>{platform === 'android' ? 'Android' : 'iOS'}</Text>
    ),
  },
  {
    title: '系统版本',
    dataIndex: 'os_version',
    key: 'os_version',
    width: 120,
  },
  {
    title: '状态',
    dataIndex: 'status',
    key: 'status',
    width: 100,
    render: (status: Device['status']) => <StatusTag status={status} type="device" />,
  },
  {
    title: '最后心跳',
    dataIndex: 'last_heartbeat',
    key: 'last_heartbeat',
    width: 180,
    render: (val: string | undefined) => formatRelativeTime(val),
  },
];

// ---------------------------------------------------------------------------
// DevicesPage
// ---------------------------------------------------------------------------

/**
 * Device management page with table, auto-refresh (5s polling),
 * and a manual discovery button.
 */
const DevicesPage: React.FC = () => {
  const { data: devices, isLoading, isError } = useDevices();
  const { mutateAsync: discover, isPending: isDiscovering } = useDiscoverDevices();

  const handleDiscover = async () => {
    try {
      // TODO: Call discoverDevices mutation
      await discover();
      message.success('设备发现已触发');
    } catch {
      message.error('设备发现失败');
    }
  };

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <Title level={4} style={{ margin: 0 }}>
          设备管理
        </Title>
        <Space>
          <Text type="secondary">自动刷新中 (5s)</Text>
          <Button
            type="primary"
            icon={<ReloadOutlined />}
            onClick={handleDiscover}
            loading={isDiscovering}
          >
            发现设备
          </Button>
        </Space>
      </div>

      {isError && (
        <Alert
          message="加载设备列表失败"
          type="error"
          showIcon
          style={{ marginBottom: 16 }}
        />
      )}

      <Card>
        <Table
          dataSource={devices}
          columns={columns}
          rowKey="id"
          loading={isLoading}
          pagination={false}
          locale={{ emptyText: '暂无设备数据' }}
        />
      </Card>
    </div>
  );
};

export default DevicesPage;
