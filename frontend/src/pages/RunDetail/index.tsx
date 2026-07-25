import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Card, Table, Descriptions, Modal, Typography, Spin, Button, Progress, Result } from 'antd';
import { ArrowLeftOutlined } from '@ant-design/icons';
import StatusTag from '@/components/StatusTag';
import LogViewer from '@/components/LogViewer';
import { useBatchDetail } from '@/hooks/useRuns';
import type { TestRun } from '@/types';

const { Title, Text } = Typography;

/**
 * Batch detail page showing batch overview, per-case results table,
 * and a log viewer modal for individual test runs.
 */
const RunDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { data, isLoading, isError } = useBatchDetail(id!);
  const [logModalVisible, setLogModalVisible] = useState(false);
  const [selectedRun, setSelectedRun] = useState<TestRun | null>(null);

  const handleViewLog = (run: TestRun) => {
    setSelectedRun(run);
    setLogModalVisible(true);
  };

  // Calculate progress
  const totalRuns = data?.batch?.test_run_count ?? 0;
  const completedRuns = (data?.batch?.passed_count ?? 0) + (data?.batch?.failed_count ?? 0) + (data?.batch?.error_count ?? 0);
  const progressPercent = totalRuns > 0 ? Math.round((completedRuns / totalRuns) * 100) : 0;

  const columns = [
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
      width: 100,
      render: (status: TestRun['status']) => <StatusTag status={status} type="run" />,
    },
    {
      title: '设备',
      dataIndex: 'device_name',
      key: 'device_name',
      width: 150,
      render: (val: string | undefined) => val || '-',
    },
    {
      title: '开始时间',
      dataIndex: 'started_at',
      key: 'started_at',
      width: 180,
      render: (val: string | undefined) => val || '-',
    },
    {
      title: '耗时(ms)',
      dataIndex: 'duration_ms',
      key: 'duration_ms',
      width: 120,
      render: (val: number | undefined) => (val != null ? val.toLocaleString() : '-'),
    },
    {
      title: '操作',
      key: 'actions',
      width: 100,
      render: (_: unknown, record: TestRun) => (
        <a onClick={() => handleViewLog(record)}>查看日志</a>
      ),
    },
  ];

  if (!id) {
    return <div>无效的批次 ID</div>;
  }

  if (isError) {
    return (
      <Result
        status="error"
        title="加载执行详情失败"
        subTitle="请检查批次 ID 是否正确或刷新页面重试"
        extra={
          <Button type="primary" onClick={() => navigate('/runs')}>
            返回执行面板
          </Button>
        }
      />
    );
  }

  return (
    <div>
      <div style={{ display: 'flex', alignItems: 'center', marginBottom: 24 }}>
        <Button
          type="text"
          icon={<ArrowLeftOutlined />}
          onClick={() => navigate('/runs')}
          style={{ marginRight: 12 }}
        >
          返回
        </Button>
        <Title level={4} style={{ margin: 0 }}>执行详情</Title>
      </div>

      {isLoading ? (
        <div style={{ textAlign: 'center', padding: 48 }}>
          <Spin size="large" />
        </div>
      ) : (
        <>
          {/* Batch overview */}
          <Card title="批次概览" style={{ marginBottom: 16 }}>
            <Descriptions column={3} size="small">
              <Descriptions.Item label="批次名称">
                {data?.batch.name || '-'}
              </Descriptions.Item>
              <Descriptions.Item label="状态">
                {data?.batch.status && <StatusTag status={data.batch.status} type="batch" />}
              </Descriptions.Item>
              <Descriptions.Item label="触发人">
                {data?.batch.triggered_by || '-'}
              </Descriptions.Item>
              <Descriptions.Item label="总数">
                {data?.batch.test_run_count ?? '-'}
              </Descriptions.Item>
              <Descriptions.Item label="通过">
                <Text type="success">{data?.batch.passed_count ?? '-'}</Text>
              </Descriptions.Item>
              <Descriptions.Item label="失败">
                <Text type="danger">{data?.batch.failed_count ?? '-'}</Text>
              </Descriptions.Item>
              <Descriptions.Item label="错误">
                <Text type="warning">{data?.batch.error_count ?? '-'}</Text>
              </Descriptions.Item>
            </Descriptions>

            {/* Progress bar */}
            {totalRuns > 0 && (
              <div style={{ marginTop: 16 }}>
                <Progress
                  percent={progressPercent}
                  format={() => `${completedRuns} / ${totalRuns}`}
                  strokeColor={{
                    '0%': '#1677ff',
                    '100%': '#52c41a',
                  }}
                />
              </div>
            )}
          </Card>

          {/* Per-case results */}
          <Card title="用例执行结果">
            <Table
              dataSource={data?.runs}
              columns={columns}
              rowKey="id"
              pagination={false}
              size="middle"
              locale={{ emptyText: '暂无执行记录' }}
            />
          </Card>

          {/* Log modal */}
          <Modal
            title={`日志 - ${selectedRun?.test_case_name || ''}`}
            open={logModalVisible}
            onCancel={() => {
              setLogModalVisible(false);
              setSelectedRun(null);
            }}
            footer={null}
            width={800}
            destroyOnClose
          >
            <LogViewer log={selectedRun?.log || '日志内容待实现'} loading={false} />
          </Modal>
        </>
      )}
    </div>
  );
};

export default RunDetailPage;
