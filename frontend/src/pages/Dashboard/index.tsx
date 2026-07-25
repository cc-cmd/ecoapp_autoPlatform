import React from 'react';
import { Row, Col, Card, Table, Typography, Spin, Result, Button } from 'antd';
import {
  BugOutlined,
  CheckCircleOutlined,
  CloseCircleOutlined,
  PlayCircleOutlined,
} from '@ant-design/icons';
import StatCard from '@/components/StatCard';
import StatusTag from '@/components/StatusTag';
import { useReportSummary } from '@/hooks/useReports';
import type { TestRun } from '@/types';

const { Title } = Typography;

// Columns for the recent runs table
const recentRunColumns = [
  {
    title: '用例名称',
    dataIndex: 'test_case_name',
    key: 'test_case_name',
    ellipsis: true,
  },
  {
    title: '状态',
    dataIndex: 'status',
    key: 'status',
    render: (status: TestRun['status']) => <StatusTag status={status} type="run" />,
  },
  {
    title: '执行时间',
    dataIndex: 'started_at',
    key: 'started_at',
    render: (val: string | undefined) => val || '-',
  },
  {
    title: '耗时(ms)',
    dataIndex: 'duration_ms',
    key: 'duration_ms',
    render: (val: number | undefined) => (val != null ? val.toLocaleString() : '-'),
  },
];

/**
 * Dashboard page showing summary statistics and recent execution records.
 */
const DashboardPage: React.FC = () => {
  const { data: summary, isLoading, isError } = useReportSummary(7);

  // TODO: Replace with actual recent runs data when API is ready
  const recentRuns: TestRun[] = [];

  if (isError) {
    return (
      <Result
        status="error"
        title="加载数据概览失败"
        subTitle="请检查网络连接或刷新页面重试"
        extra={
          <Button type="primary" onClick={() => window.location.reload()}>
            刷新页面
          </Button>
        }
      />
    );
  }

  return (
    <div>
      <Title level={4} style={{ marginBottom: 24 }}>
        数据概览
      </Title>

      {/* Stat cards */}
      <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
        <Col xs={24} sm={12} lg={6}>
          <StatCard
            title="总用例数"
            value={summary?.total_cases ?? 0}
            loading={isLoading}
            icon={<BugOutlined />}
          />
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <StatCard
            title="自动化用例"
            value={summary?.automated_cases ?? 0}
            loading={isLoading}
            icon={<PlayCircleOutlined />}
          />
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <StatCard
            title="通过率"
            value={summary ? `${(summary.pass_rate * 100).toFixed(1)}%` : '0%'}
            loading={isLoading}
            icon={<CheckCircleOutlined />}
            trend={summary ? { type: summary.pass_rate >= 0.8 ? 'up' : 'down', value: summary.pass_rate >= 0.8 ? '良好' : '偏低' } : undefined}
          />
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <StatCard
            title="失败率"
            value={summary ? `${(summary.fail_rate * 100).toFixed(1)}%` : '0%'}
            loading={isLoading}
            icon={<CloseCircleOutlined />}
            trend={summary && summary.fail_rate > 0.2 ? { type: 'down', value: '偏高' } : undefined}
          />
        </Col>
      </Row>

      {/* Recent runs */}
      <Card title="最近执行记录">
        {isLoading ? (
          <div style={{ textAlign: 'center', padding: 24 }}>
            <Spin />
          </div>
        ) : (
          <Table
            dataSource={recentRuns}
            columns={recentRunColumns}
            rowKey="id"
            pagination={false}
            locale={{ emptyText: '暂无执行记录' }}
          />
        )}
      </Card>
    </div>
  );
};

export default DashboardPage;
