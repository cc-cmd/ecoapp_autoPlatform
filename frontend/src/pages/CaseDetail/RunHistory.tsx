import React from 'react';
import { Table, Typography } from 'antd';
import StatusTag from '@/components/StatusTag';
import { useCaseRuns } from '@/hooks/useCases';
import type { TestRun } from '@/types';

const { Text } = Typography;

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

interface RunHistoryProps {
  /** Test case ID to fetch history for. */
  caseId: string;
}

// ---------------------------------------------------------------------------
// Columns
// ---------------------------------------------------------------------------

const columns = [
  {
    title: '批次ID',
    dataIndex: 'run_group_id',
    key: 'run_group_id',
    ellipsis: true,
    width: 200,
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
    title: '错误信息',
    dataIndex: 'error_message',
    key: 'error_message',
    ellipsis: true,
    render: (val: string | undefined) =>
      val ? <Text type="danger">{val}</Text> : '-',
  },
];

// ---------------------------------------------------------------------------
// RunHistory
// ---------------------------------------------------------------------------

/**
 * Table showing past execution runs for a specific test case.
 */
const RunHistory: React.FC<RunHistoryProps> = ({ caseId }) => {
  const { data, isLoading } = useCaseRuns(caseId);

  return (
    <Table
      dataSource={data?.items}
      columns={columns}
      rowKey="id"
      loading={isLoading}
      pagination={{
        pageSize: 10,
        total: data?.total ?? 0,
        showSizeChanger: false,
        showTotal: (total) => `共 ${total} 条`,
      }}
      size="small"
      locale={{ emptyText: '暂无执行记录' }}
    />
  );
};

export default RunHistory;
