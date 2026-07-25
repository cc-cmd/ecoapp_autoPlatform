import React from 'react';
import { Card, Skeleton, Typography, Space } from 'antd';
import { CaretUpOutlined, CaretDownOutlined } from '@ant-design/icons';

const { Text, Title } = Typography;

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

interface TrendInfo {
  type: 'up' | 'down';
  value: string;
}

interface StatCardProps {
  /** Card title. */
  title: string;
  /** Numeric value to display. */
  value: number | string;
  /** Whether the data is still loading. */
  loading?: boolean;
  /** Icon to show alongside the value. */
  icon?: React.ReactNode;
  /** Trend direction with display value. */
  trend?: TrendInfo;
}

// ---------------------------------------------------------------------------
// StatCard
// ---------------------------------------------------------------------------

/**
 * Statistics summary card with icon, value, and optional trend indicator.
 * Shows a skeleton placeholder while loading.
 */
const StatCard: React.FC<StatCardProps> = ({ title, value, loading = false, icon, trend }) => {
  return (
    <Card hoverable>
      {loading ? (
        <Skeleton active paragraph={{ rows: 1 }} />
      ) : (
        <Space direction="vertical" size={4} style={{ width: '100%' }}>
          <Text type="secondary">{title}</Text>
          <Space>
            {icon && <span style={{ fontSize: 24, opacity: 0.65 }}>{icon}</span>}
            <Title level={3} style={{ margin: 0 }}>
              {value}
            </Title>
            {trend && trend.type === 'up' && (
              <Text type="success" className="stat-card-trend-up">
                <CaretUpOutlined /> {trend.value}
              </Text>
            )}
            {trend && trend.type === 'down' && (
              <Text type="danger" className="stat-card-trend-down">
                <CaretDownOutlined /> {trend.value}
              </Text>
            )}
          </Space>
        </Space>
      )}
    </Card>
  );
};

export default StatCard;
