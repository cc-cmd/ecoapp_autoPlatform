import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Table, Button, Space, message, Tooltip, Alert } from 'antd';
import { StopOutlined, EyeOutlined } from '@ant-design/icons';
import StatusTag from '@/components/StatusTag';
import { useBatches, useCancelBatch } from '@/hooks/useRuns';
import type { RunGroup } from '@/types';

// ---------------------------------------------------------------------------
// Columns
// ---------------------------------------------------------------------------

interface RunQueueProps {
  // No additional props needed -- fetches its own data
}

/**
 * Batch queue table with auto-polling (3s interval when active batches exist).
 * Shows execution batches and allows cancellation.
 */
const RunQueue: React.FC<RunQueueProps> = () => {
  const navigate = useNavigate();
  const { data, isLoading, isError } = useBatches({ page: 1, size: 50 });
  const { mutateAsync: cancelBatch, isPending: isCancelling } = useCancelBatch();

  const handleCancel = async (batchId: string) => {
    try {
      // TODO: Call cancelBatch mutation
      await cancelBatch(batchId);
      message.success('已发送取消请求');
    } catch {
      message.error('取消失败');
    }
  };

  const columns = [
    {
      title: '批次名称',
      dataIndex: 'name',
      key: 'name',
      ellipsis: true,
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      width: 110,
      render: (status: RunGroup['status']) => <StatusTag status={status} type="batch" />,
    },
    {
      title: '总数',
      dataIndex: 'test_run_count',
      key: 'test_run_count',
      width: 80,
    },
    {
      title: '通过',
      dataIndex: 'passed_count',
      key: 'passed_count',
      width: 80,
    },
    {
      title: '失败',
      dataIndex: 'failed_count',
      key: 'failed_count',
      width: 80,
    },
    {
      title: '错误',
      dataIndex: 'error_count',
      key: 'error_count',
      width: 80,
    },
    {
      title: '触发时间',
      dataIndex: 'created_at',
      key: 'created_at',
      width: 180,
    },
    {
      title: '操作',
      key: 'actions',
      width: 120,
      render: (_: unknown, record: RunGroup) => (
        <Space>
          <Tooltip title="查看详情">
            <Button
              type="link"
              size="small"
              icon={<EyeOutlined />}
              onClick={() => navigate(`/runs/${record.id}`)}
            />
          </Tooltip>
          {record.status !== 'completed' && (
            <Tooltip title="取消批次">
              <Button
                type="link"
                size="small"
                danger
                icon={<StopOutlined />}
                loading={isCancelling}
                onClick={() => handleCancel(record.id)}
              />
            </Tooltip>
          )}
        </Space>
      ),
    },
  ];

  return (
    <div>
      {isError && (
        <Alert
          message="加载执行队列失败"
          type="error"
          showIcon
          style={{ marginBottom: 16 }}
        />
      )}
      <Table
        dataSource={data?.items}
        columns={columns}
        rowKey="id"
        loading={isLoading}
        pagination={{
          pageSize: 20,
          total: data?.total ?? 0,
          showSizeChanger: false,
          showTotal: (total) => `共 ${total} 批`,
        }}
        size="middle"
        locale={{ emptyText: '暂无执行记录' }}
      />
    </div>
  );
};

export default RunQueue;
